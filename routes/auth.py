from fastapi import APIRouter, HTTPException
from db import get_connection

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.user_id,
            u.username,
            r.role_name
        FROM users u
        JOIN roles r
            ON u.role_id = r.role_id
        WHERE
            u.username = :1
            AND u.password = :2
    """, [
        data["username"],
        data["password"]
    ])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    return {
        "user_id": row[0],
        "username": row[1],
        "role": row[2]
    }