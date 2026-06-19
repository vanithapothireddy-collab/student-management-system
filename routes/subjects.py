from fastapi import APIRouter
from db import get_connection

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

@router.get("/")
def get_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            subject_id,
            subject_name
        FROM subjects
        ORDER BY subject_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "subject_id": row[0],
            "subject_name": row[1]
        })

    cursor.close()
    conn.close()

    return result