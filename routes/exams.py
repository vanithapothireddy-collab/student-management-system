from fastapi import APIRouter
from db import get_connection

router = APIRouter(
    prefix="/exams",
    tags=["Exams"]
)

@router.get("/")
def get_exams():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            exam_id,
            subject_id,
            exam_name,
            exam_date
        FROM exams
        ORDER BY exam_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "exam_id": row[0],
            "subject_id": row[1],
            "exam_name": row[2],
            "exam_date": str(row[3])
        })

    cursor.close()
    conn.close()

    return result