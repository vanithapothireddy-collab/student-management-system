from fastapi import APIRouter, Header, HTTPException
from db import get_connection


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

def verify_admin(role: str):

    if role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Access Denied"
        )
    


@router.get("/")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM v_student_dashboard
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


@router.get("/student-count")
def student_count():

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


@router.get("/department-strength")
def department_strength():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.department_name,
            COUNT(s.student_id)
        FROM departments d
        LEFT JOIN students s
            ON d.department_id = s.department_id
        GROUP BY d.department_name
        ORDER BY d.department_name
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "department_name": row[0],
            "student_count": row[1]
        })

    cursor.close()
    conn.close()

    return result
@router.get("/fee-summary")
def fee_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT NVL(SUM(amount), 0)
        FROM student_fees
    """)

    total_fee = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_fee_collected": total_fee
    }

@router.get("/management-dashboard")
def management_dashboard(role: str = Header()):

    verify_admin(role)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM v_management_dashboard
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

@router.get("/top-students")
def top_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_name,
            ROUND(AVG(m.marks_obtained), 2) avg_marks
        FROM students s
        JOIN marks m
            ON s.student_id = m.student_id
        GROUP BY s.student_name
        ORDER BY avg_marks DESC
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "student_name": row[0],
            "average_marks": row[1]
        })

    cursor.close()
    conn.close()

    return result
@router.get("/test-db")
def test_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT USER FROM dual")
    user = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {"user": user}
@router.get("/top-students")
def top_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM (
            SELECT
                s.student_name,
                SUM(m.marks_obtained) AS total_marks
            FROM students s
            JOIN marks m
                ON s.student_id = m.student_id
            GROUP BY s.student_name
            ORDER BY SUM(m.marks_obtained) DESC
        )
        WHERE ROWNUM <= 5
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

@router.get("/student-performance")
def student_performance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM v_student_performance
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

@router.get("/top-rankers")
def top_rankers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM (
            SELECT
                student_name,
                ROUND(AVG(marks_obtained),2) avg_marks
            FROM students s
            JOIN marks m
                ON s.student_id = m.student_id
            GROUP BY student_name
            ORDER BY avg_marks DESC
        )
        WHERE ROWNUM <= 5
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
