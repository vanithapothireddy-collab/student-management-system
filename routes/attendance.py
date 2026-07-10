from fastapi import APIRouter
from db import get_connection
from models.attendance import AttendanceCreate

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)

@router.get("/")
def get_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.attendance_id,
            s.student_name,
            sub.subject_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        ORDER BY a.attendance_date DESC
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "attendance_id": row[0],
            "student_name": row[1],
            "subject_name": row[2],
            "attendance_date": str(row[3]),
            "status": row[4]

        })

    cursor.close()
    conn.close()

    return result

@router.post("/")
def create_attendance(attendance: AttendanceCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (
            attendance_id,
            student_id,
            subject_id,
            attendance_date,
            status
        )
        VALUES
        (
            attendance_seq.NEXTVAL,
            :1,
            :2,
            :3,
            :4
        )
    """,
    (
        attendance.student_id,
        attendance.subject_id,
        attendance.attendance_date,
        attendance.status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Attendance Saved Successfully"
    }
@router.get("/{attendance_id}")
def get_attendance_by_id(attendance_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            attendance_id,
            student_id,
            subject_id,
            attendance_date,
            status
        FROM attendance
        WHERE attendance_id=:1
    """,(attendance_id,))

    row=cursor.fetchone()

    cursor.close()
    conn.close()

    return{
        "attendance_id":row[0],
        "student_id":row[1],
        "subject_id":row[2],
        "attendance_date":str(row[3]),
        "status":row[4]
    }
@router.put("/{attendance_id}")
def update_attendance(attendance_id:int,attendance:AttendanceCreate):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE attendance
        SET
            student_id=:1,
            subject_id=:2,
            attendance_date=:3,
            status=:4
        WHERE attendance_id=:5
    """,
    (
        attendance.student_id,
        attendance.subject_id,
        attendance.attendance_date,
        attendance.status,
        attendance_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return{
        "message":"Attendance Updated Successfully"
    }
@router.delete("/{attendance_id}")
def delete_attendance(attendance_id:int):

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
        DELETE FROM attendance
        WHERE attendance_id=:1
    """,(attendance_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return{
        "message":"Attendance Deleted Successfully"
    }