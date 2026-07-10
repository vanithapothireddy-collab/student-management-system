from fastapi import APIRouter
from db import get_connection
from openpyxl import Workbook
from fastapi.responses import FileResponse
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# -----------------------------------
# Student Report
# -----------------------------------

@router.get("/students")
def student_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_id,
            s.student_name,
            d.department_name,
            b.batch_name

        FROM students s

        JOIN departments d
            ON s.department_id = d.department_id

        JOIN batches b
            ON s.batch_id = b.batch_id

        ORDER BY s.student_id

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# -----------------------------------
# Department Report
# -----------------------------------

@router.get("/departments")
def department_report():

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


# -----------------------------------
# Attendance Report
# -----------------------------------

@router.get("/attendance")
def attendance_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_name,
            a.attendance_date,
            a.status

        FROM attendance a

        JOIN students s

            ON a.student_id = s.student_id

        ORDER BY a.attendance_date DESC

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# -----------------------------------
# Fee Report
# -----------------------------------

@router.get("/fees")
def fee_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_name,
            f.total_fee,
            f.paid_fee,
            f.status

        FROM fees f

        JOIN students s

            ON f.student_id = s.student_id

        ORDER BY s.student_name

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


# -----------------------------------
# Marks Report
# -----------------------------------

@router.get("/marks")
def marks_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_name,
            e.exam_name,
            m.marks_obtained

        FROM marks m

        JOIN students s

            ON m.student_id = s.student_id

        JOIN exams e

            ON m.exam_id = e.exam_id

        ORDER BY s.student_name

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
@router.get("/students/excel")
def export_students_excel():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_id,
            s.student_name,
            d.department_name,
            b.batch_name

        FROM students s

        JOIN departments d
            ON s.department_id = d.department_id

        JOIN batches b
            ON s.batch_id = b.batch_id

        ORDER BY s.student_id

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    wb = Workbook()

    ws = wb.active

    ws.title = "Students"

    ws.append([
        "Student ID",
        "Student Name",
        "Department",
        "Batch"
    ])

    for row in rows:

        ws.append(row)

    filename = "student_report.xlsx"

    wb.save(filename)

    return FileResponse(

        path=filename,

        filename=filename,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
@router.get("/students/pdf")
def export_students_pdf():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_id,
            s.student_name,
            d.department_name,
            b.batch_name

        FROM students s

        JOIN departments d
            ON s.department_id = d.department_id

        JOIN batches b
            ON s.batch_id = b.batch_id

        ORDER BY s.student_id

    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    filename = "student_report.pdf"

    pdf = SimpleDocTemplate(filename)

    data = [
        ["Student ID", "Student Name", "Department", "Batch"]
    ]

    for row in rows:
        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("BACKGROUND", (0,1), (-1,-1), colors.beige),

        ("ALIGN", (0,0), (-1,-1), "CENTER"),

        ("BOTTOMPADDING", (0,0), (-1,0), 10),

    ]))

    pdf.build([table])

    return FileResponse(

        filename,

        filename=filename,

        media_type="application/pdf"

    )