from fastapi import APIRouter
from db import get_connection

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
            mark_id,
            student_id,
            exam_id,
            marks_obtained
        FROM marks
        ORDER BY mark_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "mark_id": row[0],
            "student_id": row[1],
            "exam_id": row[2],
            "marks_obtained": row[3]
        })

    cursor.close()
    conn.close()

    return result