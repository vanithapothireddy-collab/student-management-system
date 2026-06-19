from fastapi import APIRouter
from db import get_connection

router = APIRouter(
    prefix="/fees",
    tags=["Fees"]
)

@router.get("/")
def get_fees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM fees
        ORDER BY fee_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "fee_id": row[0],
            "student_id": row[1],
            "amount": row[2],
            "status": row[3]
        })

    cursor.close()
    conn.close()

    return result