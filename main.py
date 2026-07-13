from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db import get_connection

from routes.students import router as student_router
from routes.departments import router as department_router
from routes.subjects import router as subject_router
from routes.exams import router as exam_router
from routes.marks import router as marks_router
from routes.fees import router as fee_router
from routes.dashboard import router as dashboard_router
from routes.attendance import router as attendance_router
from routes.auth import router as auth_router
from routes.batches import router as batch_router
from routes.reports import router as reports_router
from routes.teachers import router as teacher_router
from routes.teacher_subjects import router as teacher_subject_router

app = FastAPI(
    title="Student Management System",
    version="1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve CSS and JavaScript
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(student_router)
app.include_router(department_router)
app.include_router(subject_router)
app.include_router(exam_router)
app.include_router(marks_router)
app.include_router(fee_router)
app.include_router(dashboard_router)
app.include_router(attendance_router)
app.include_router(auth_router)
app.include_router(batch_router)
app.include_router(reports_router)
app.include_router(teacher_router)
app.include_router(teacher_subject_router)

# Home page
@app.get("/")
def home():
    return FileResponse("templates/index.html")

@app.get("/students.html")
def students_page():
    return FileResponse("templates/students.html")


@app.get("/departments.html")
def departments_page():
    return FileResponse("templates/departments.html")


@app.get("/subjects.html")
def subjects_page():
    return FileResponse("templates/subjects.html")


@app.get("/attendance.html")
def attendance_page():
    return FileResponse("templates/attendance.html")


@app.get("/exams.html")
def exams_page():
    return FileResponse("templates/exams.html")


@app.get("/marks.html")
def marks_page():
    return FileResponse("templates/marks.html")

@app.get("/batches.html")
def batches_page():
    return FileResponse("templates/batches.html")

@app.get("/reports.html")
def reports_page():
    return FileResponse("templates/reports.html")

@app.get("/fees.html")
def fees_page():
    return FileResponse("templates/fees.html")
# Database test
@app.get("/db-test")
def db_test():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 'Oracle Connected' FROM dual")
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"message": result[0]}
@app.get("/login")
def login_page():

    return FileResponse("templates/login.html")
@app.get("/teachers.html")
def teachers_page():
    return FileResponse("templates/teachers.html")
@app.get("/teacher-subjects.html")
def teacher_subject_page():
    return FileResponse("templates/teacher_subjects.html")
@app.get("/dashboard.html")
def dashboard_page():
    return FileResponse("templates/dashboard.html")