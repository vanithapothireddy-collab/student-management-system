from fastapi import APIRouter
from db import get_connection
from models.marks import MarkCreate

router = APIRouter(
    prefix="/marks",
    tags=["Marks"]
)


@router.get("/")
def get_marks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.mark_id,
            s.student_name,
            e.exam_name,
            m.marks_obtained,
            m.student_id,
            m.exam_id
        FROM marks m
        JOIN students s
            ON m.student_id = s.student_id
        JOIN exams e
            ON m.exam_id = e.exam_id
        ORDER BY m.mark_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        marks = row[3]
        student_id = row[4]
        exam_id = row[5]

        if marks >= 90:
            grade = "A"
        elif marks >= 80:
            grade = "B"
        elif marks >= 70:
            grade = "C"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"

        result.append({
            "mark_id": row[0],
            "student_id": student_id,
            "exam_id": exam_id,
            "student_name": row[1],
            "exam_name": row[2],
            "marks": marks,
            "marks_obtained": marks,
            "grade": grade
        })

    cursor.close()
    conn.close()

    return result


@router.post("/")
def create_mark(mark: MarkCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO marks
        (
            mark_id,
            student_id,
            exam_id,
            marks_obtained
        )
        VALUES
        (
            MARK_SEQ.NEXTVAL,
            :1,
            :2,
            :3
        )
    """, (
        mark.student_id,
        mark.exam_id,
        mark.marks_obtained
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Marks Added Successfully"
    }


@router.get("/{mark_id}")
def get_mark(mark_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            mark_id,
            student_id,
            exam_id,
            marks_obtained
        FROM marks
        WHERE mark_id = :1
    """, (mark_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return {"message": "Mark not found"}

    return {
        "mark_id": row[0],
        "student_id": row[1],
        "exam_id": row[2],
        "marks_obtained": row[3]
    }


@router.put("/{mark_id}")
def update_mark(mark_id: int, mark: MarkCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE marks
        SET
            student_id = :1,
            exam_id = :2,
            marks_obtained = :3
        WHERE mark_id = :4
    """, (
        mark.student_id,
        mark.exam_id,
        mark.marks_obtained,
        mark_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Marks Updated Successfully"
    }


@router.delete("/{mark_id}")
def delete_mark(mark_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM marks
        WHERE mark_id = :1
    """, (mark_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Marks Deleted Successfully"
    }


@router.get("/search/{student_name}")
def search_marks(student_name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.mark_id,
            s.student_name,
            e.exam_name,
            m.marks_obtained,
            m.student_id,
            m.exam_id
        FROM marks m
        JOIN students s
            ON m.student_id = s.student_id
        JOIN exams e
            ON m.exam_id = e.exam_id
        WHERE UPPER(s.student_name) LIKE UPPER(:1)
        ORDER BY m.mark_id
    """, ('%' + student_name + '%',))

    rows = cursor.fetchall()

    result = []

    for row in rows:

        marks = row[3]

        if marks >= 90:
            grade = "A"
        elif marks >= 80:
            grade = "B"
        elif marks >= 70:
            grade = "C"
        elif marks >= 60:
            grade = "D"
        else:
            grade = "F"

        result.append({
            "mark_id": row[0],
            "student_id": row[4],
            "exam_id": row[5],
            "student_name": row[1],
            "exam_name": row[2],
            "marks": marks,
            "grade": grade
        })

    cursor.close()
    conn.close()

    return result