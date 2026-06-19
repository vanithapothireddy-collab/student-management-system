from fastapi import APIRouter
from db import get_connection

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.get("/")
def get_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM attendance
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows