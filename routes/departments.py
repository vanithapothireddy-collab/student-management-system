from fastapi import APIRouter
from db import get_connection

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.get("/")
def get_departments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT department_id,
               department_name
        FROM departments
        ORDER BY department_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "department_id": row[0],
            "department_name": row[1]
        })

    cursor.close()
    conn.close()

    return result