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

    try:
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

    except Exception as e:
        import traceback
        traceback.print_exc()

        return {
            "error": str(e)
        }
@router.get("/subject-count")
def subject_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM subjects
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_subjects": count
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
        SELECT NVL(SUM(paid_fee), 0)
        FROM fees
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
@router.get("/recent-students")
def recent_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM
    (
        SELECT
            s.student_id,
            s.student_name,
            d.department_name
        FROM students s
        JOIN departments d
            ON s.department_id = d.department_id
        ORDER BY s.student_id DESC
    )
    WHERE ROWNUM <= 5
""")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
@router.get("/department-count")
def department_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM departments
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_departments": count
    }
@router.get("/department-wise-students")
def department_wise_students():

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

    cursor.close()
    conn.close()

    return rows
@router.get("/present-today")
def present_today():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = TRUNC(SYSDATE)
        AND status='Present'
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "present_today": count
    }
@router.get("/absent-today")
def absent_today():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE attendance_date = TRUNC(SYSDATE)
        AND status='Absent'
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "absent_today": count
    }
@router.get("/attendance-percentage")
def attendance_percentage():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            ROUND(

                SUM(

                    CASE

                        WHEN status='Present'

                        THEN 1

                        ELSE 0

                    END

                )

                /

                COUNT(*)*100,

            2)

        FROM attendance

    """)

    percentage = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "attendance_percentage":

        percentage if percentage else 0

    }
@router.get("/marks-count")
def marks_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM marks

    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "total_marks": total

    }
@router.get("/teacher-count")
def teacher_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM teachers

    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "total_teachers": total

    }
@router.get("/batch-count")
def batch_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM batches

    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "total_batches": total

    }
@router.get("/exam-count")
def exam_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM exams

    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "total_exams": total

    }
@router.get("/fee-chart")
def fee_chart():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            s.student_name,
            sf.amount
        FROM student_fees sf
        JOIN students s
            ON sf.student_id = s.student_id
        ORDER BY sf.student_id

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
@router.get("/attendance-chart")
def attendance_chart():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            status,
            COUNT(*)
        FROM attendance
        GROUP BY status
        ORDER BY status

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows