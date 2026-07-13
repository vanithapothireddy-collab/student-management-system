from fastapi import APIRouter
from db import get_connection
from models.teacher_subject import TeacherSubjectCreate

router = APIRouter(
    prefix="/teacher-subjects",
    tags=["Teacher Subjects"]
)
@router.get("/")
def get_assignments(page: int = 1, page_size: int = 30):

    offset = (page - 1) * page_size

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM
        (
            SELECT
                ROW_NUMBER() OVER (ORDER BY ts.assignment_id) rn,
                ts.assignment_id,
                t.teacher_name,
                s.subject_name,
                t.teacher_id,
                s.subject_id
            FROM teacher_subjects ts
            JOIN teachers t
                ON ts.teacher_id=t.teacher_id
            JOIN subjects s
                ON ts.subject_id=s.subject_id
        )
        WHERE rn BETWEEN :1 AND :2
    """, [
        offset + 1,
        offset + page_size
    ])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "assignment_id": r[1],
            "teacher_name": r[2],
            "subject_name": r[3],
            "teacher_id": r[4],
            "subject_id": r[5]
        }
        for r in rows
    ]
@router.post("/")
def add_assignment(data:TeacherSubjectCreate):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        INSERT INTO teacher_subjects
        VALUES
        (
            teacher_subject_seq.NEXTVAL,
            :1,
            :2
        )
    """,[data.teacher_id,data.subject_id])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message":"Assignment Added"}
@router.put("/{assignment_id}")
def update_assignment(assignment_id: int, data: TeacherSubjectCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teacher_subjects
        SET
            teacher_id = :1,
            subject_id = :2
        WHERE assignment_id = :3
    """, [
        data.teacher_id,
        data.subject_id,
        assignment_id
    ])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Assignment Updated"}
@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM teacher_subjects
        WHERE assignment_id = :1
    """, [assignment_id])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Assignment Deleted"}
@router.get("/search/{keyword}")
def search_assignment(keyword: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ts.assignment_id,
            t.teacher_name,
            s.subject_name,
            t.teacher_id,
            s.subject_id
        FROM teacher_subjects ts
        JOIN teachers t
            ON ts.teacher_id = t.teacher_id
        JOIN subjects s
            ON ts.subject_id = s.subject_id
        WHERE
            UPPER(t.teacher_name) LIKE UPPER(:1)
            OR UPPER(s.subject_name) LIKE UPPER(:1)
        ORDER BY ts.assignment_id
    """, [f"%{keyword}%"])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "assignment_id": r[0],
            "teacher_name": r[1],
            "subject_name": r[2],
            "teacher_id": r[3],
            "subject_id": r[4]
        }
        for r in rows
    ]
@router.get("/{assignment_id}")
def get_assignment(assignment_id:int):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        SELECT
            assignment_id,
            teacher_id,
            subject_id
        FROM teacher_subjects
        WHERE assignment_id=:1
    """,[assignment_id])

    row=cursor.fetchone()

    cursor.close()
    conn.close()

    return{
        "assignment_id":row[0],
        "teacher_id":row[1],
        "subject_id":row[2]
    }
@router.get("/dashboard/total-assignments")
def total_assignments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM teacher_subjects
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_assignments": total
    }
@router.get("/dashboard/total-teachers")
def total_teachers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM teachers
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_teachers": total
    }
@router.get("/dashboard/total-subjects")
def total_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM subjects
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_subjects": total
    }
@router.get("/count")
def assignment_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM teacher_subjects

    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "count": total

    }