from fastapi import APIRouter
from pydantic import BaseModel
from db import get_connection

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user: LoginRequest):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role
        FROM app_users
        WHERE username = :1
        AND password = :2
    """, [user.username, user.password])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "message": "Login Success",
            "role": row[0]
        }

    return {
        "message": "Invalid Username or Password"
    }

from jose import jwt

SECRET_KEY = "studentmanagementsystem"

ALGORITHM = "HS256"