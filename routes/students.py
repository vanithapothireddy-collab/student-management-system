from models.student import StudentCreate
from fastapi import APIRouter, HTTPException
from db import get_connection
from logger_config import logger

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/")
def get_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            student_name,
            gender,
            department_id,
            batch_id
        FROM students
        ORDER BY student_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_id": row[3],
            "batch_id": row[4]
        })

    cursor.close()
    conn.close()

    return result
@router.post("/")
def create_student(student: StudentCreate):
    logger.info(f"Creating student {student.student_name}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (
            student_id,
            student_name,
            gender,
            department_id,
            batch_id
        )
        VALUES
        (
            student_seq.NEXTVAL,
            :1,
            :2,
            :3,
            :4
        )
    """,
    (
        student.student_name,
        student.gender,
        student.department_id,
        student.batch_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Student Created Successfully"
    }


@router.get("/search/{name}")
def search_student(name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id,
               student_name,
               gender,
               department_id,
               batch_id
        FROM students
        WHERE UPPER(student_name)
        LIKE UPPER(:name)
    """, {"name": f"%{name}%"})

    students = []

    for row in cursor:
        students.append({
            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_id": row[3],
            "batch_id": row[4]
        })

    conn.close()

    return students

@router.get("/page/")
def get_students_paginated(page: int = 1, limit: int = 10):

    offset = (page - 1) * limit

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            student_id,
            student_name,
            gender,
            department_id,
            batch_id
        FROM (
            SELECT
                student_id,
                student_name,
                gender,
                department_id,
                batch_id,
                ROW_NUMBER() OVER (ORDER BY student_id) rn
            FROM students
        )
        WHERE rn BETWEEN {offset + 1} AND {offset + limit}
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_id": row[3],
            "batch_id": row[4]
        })

    cursor.close()
    conn.close()

    return result

@router.get("/dashboard/")
def student_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.student_name,
            d.department_name,
            f.status
        FROM students s
        LEFT JOIN departments d
            ON s.department_id = d.department_id
        LEFT JOIN fees f
            ON s.student_id = f.student_id
        ORDER BY s.student_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "student_id": row[0],
            "student_name": row[1],
            "department_name": row[2],
            "fee_status": row[3]
        })

    cursor.close()
    conn.close()

    return result
@router.get("/count/")
def get_student_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM students
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_students": count
    }

@router.get("/{student_id}")
def get_student(student_id: int):
    logger.info("TEST LOG WORKING")
    logger.info(f"Fetching student {student_id}")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            student_id,
            student_name,
            gender,
            department_id,
            batch_id
        FROM students
        WHERE student_id = :1
    """, (student_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return {
            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_id": row[3],
            "batch_id": row[4]
        }

    return {"message": "Student Not Found"}


@router.put("/{student_id}")
def update_student(student_id: int, student: StudentCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET
            student_name = :1,
            gender = :2,
            department_id = :3,
            batch_id = :4
        WHERE student_id = :5
    """,
    (
        student.student_name,
        student.gender,
        student.department_id,
        student.batch_id,
        student_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Student Updated Successfully"
    }
@router.delete("/{student_id}")
def delete_student(student_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM students
        WHERE student_id = :1
    """, (student_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Student Deleted Successfully"
    }