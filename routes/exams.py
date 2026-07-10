from fastapi import APIRouter
from db import get_connection
from pydantic import BaseModel

router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)

class Exam(BaseModel):
    subject_id: int
    exam_name: str
    exam_date: str

@router.get("/")
def get_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            e.exam_id,
            e.subject_id,
            s.subject_name,
            e.exam_name,
            TO_CHAR(e.exam_date,'YYYY-MM-DD')
        FROM exams e
        LEFT JOIN subjects s
            ON e.subject_id = s.subject_id
        WHERE e.is_active='Y'
        ORDER BY e.exam_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "exam_id": row[0],
            "subject_id": row[1],
            "subject_name": row[2],
            "exam_name": row[3],
            "exam_date": row[4]

        })

    cursor.close()
    conn.close()

    return result
@router.get("/total")
def total_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM exams
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_exams": total
    }
@router.get("/upcoming")
def upcoming_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM exams
        WHERE exam_date > TRUNC(SYSDATE)
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "upcoming_exams": total
    }
@router.get("/completed")
def completed_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM exams
        WHERE exam_date < TRUNC(SYSDATE)
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "completed_exams": total
    }
@router.get("/subjects-covered")
def subjects_covered():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT subject_id)
        FROM exams
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "subjects_covered": total
    }

@router.post("/")
def add_exam(exam: Exam):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO exams
        (exam_id, subject_id, exam_name, exam_date, is_active)
        VALUES
        (
            exam_seq.NEXTVAL,
            :1,
            :2,
            TO_DATE(:3,'YYYY-MM-DD'),
            'Y'
        )
    """,(exam.subject_id,
         exam.exam_name,
         exam.exam_date))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message":"Exam Added Successfully"}
@router.put("/{exam_id}")
def update_exam(exam_id: int, exam: Exam):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE exams
        SET
            subject_id = :1,
            exam_name = :2,
            exam_date = TO_DATE(:3,'YYYY-MM-DD')
        WHERE exam_id = :4
    """, (
        exam.subject_id,
        exam.exam_name,
        exam.exam_date,
        exam_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Exam Updated Successfully"}
@router.delete("/{exam_id}")
def delete_exam(exam_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE exams
        SET is_active='N'
        WHERE exam_id=:1
    """,(exam_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message":"Exam Deleted Successfully"}
@router.get("/search/{keyword}")
def search_exam(keyword: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            e.exam_id,
            e.subject_id,
            s.subject_name,
            e.exam_name,
            TO_CHAR(e.exam_date,'YYYY-MM-DD')
        FROM exams e
        LEFT JOIN subjects s
            ON e.subject_id = s.subject_id
        WHERE
            e.is_active='Y'
        AND
            (
                UPPER(e.exam_name) LIKE UPPER(:1)
                OR
                UPPER(s.subject_name) LIKE UPPER(:1)
            )
        ORDER BY e.exam_id
    """,('%'+keyword+'%',))

    rows = cursor.fetchall()

    result=[]

    for row in rows:

        result.append({

            "exam_id":row[0],
            "subject_id":row[1],
            "subject_name":row[2],
            "exam_name":row[3],
            "exam_date":row[4]

        })

    cursor.close()
    conn.close()

    return result
@router.get("/{exam_id}")
def get_exam(exam_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            exam_id,
            subject_id,
            exam_name,
            TO_CHAR(exam_date,'YYYY-MM-DD')
        FROM exams
        WHERE exam_id = :1
          AND is_active = 'Y'
    """, (exam_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return {"message": "Exam not found"}

    return {
        "exam_id": row[0],
        "subject_id": row[1],
        "exam_name": row[2],
        "exam_date": row[3]
    }