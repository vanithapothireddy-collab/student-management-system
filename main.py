from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.students import router as student_router
from routes.departments import router as department_router
from routes.subjects import router as subject_router
from routes.exams import router as exam_router
from routes.marks import router as marks_router
from routes.fees import router as fee_router
from routes.dashboard import router as dashboard_router
from routes.attendance import router as attendance_router
from routes.auth import router as auth_router
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

app.include_router(student_router)
app.include_router(department_router)
app.include_router(subject_router)
app.include_router(exam_router)
app.include_router(marks_router)
app.include_router(fee_router)
app.include_router(dashboard_router)
app.include_router(attendance_router)
app.include_router(auth_router)
@app.get("/")
def home():
    return {
        "message": "Student Management System Running"
    }
@app.get("/db-test")
def db_test():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 'Oracle Connected' FROM dual")

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {"message": result[0]}