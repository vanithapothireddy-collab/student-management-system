from fastapi import APIRouter
from db import get_connection
from models.teacher import TeacherCreate

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
    
)

@router.get("/dashboard/total-teachers")
def total_teachers():

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
@router.get("/dashboard/assigned-subjects")
def assigned_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(DISTINCT subject_name)
        FROM teachers
    """)

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "assigned_subjects": total
    }
@router.get("/")
def get_teachers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        teacher_id,
        teacher_name,
        subject_name,
        email
    FROM teachers
    ORDER BY teacher_id
""")

    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return [
    {
        "teacher_id": r[0],
        "teacher_name": r[1],
        "subject_name": r[2],
        "email": r[3]
    }
    for r in rows
]
@router.get("/{teacher_id}")
def get_teacher(teacher_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        teacher_id,
        teacher_name,
        subject_name,
        email
    FROM teachers
    WHERE teacher_id=:1
""",[teacher_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return {
    "teacher_id": row[0],
    "teacher_name": row[1],
    "subject_name": row[2],
    "email": row[3]
}
@router.post("/")
def add_teacher(teacher: TeacherCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
INSERT INTO teachers
(
    teacher_id,
    teacher_name,
    subject_name,
    email
)
VALUES
(
    teacher_seq.NEXTVAL,
    :1,
    :2,
    :3
)
""",[
    teacher.teacher_name,
    teacher.subject_name,
    teacher.email
])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message":"Teacher Added Successfully"}
@router.delete("/{teacher_id}")
def delete_teacher(teacher_id:int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM teachers

        WHERE teacher_id=:1

    """, [teacher_id])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message":"Teacher Deleted Successfully"}
@router.put("/{teacher_id}")
def update_teacher(teacher_id: int, teacher: TeacherCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teachers
        SET
            teacher_name = :1,
            subject_name = :2,
            email = :3
        WHERE teacher_id = :4
    """, [
        teacher.teacher_name,
        teacher.subject_name,
        teacher.email,
        teacher_id
    ])

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Teacher Updated Successfully"}
@router.get("/search/{keyword}")
def search_teacher(keyword: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            teacher_id,
            teacher_name,
            subject_name,
            email
        FROM teachers
        WHERE
            UPPER(teacher_name) LIKE UPPER(:1)
            OR UPPER(subject_name) LIKE UPPER(:1)
        ORDER BY teacher_id
    """, [f"%{keyword}%"])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "teacher_id": r[0],
            "teacher_name": r[1],
            "subject_name": r[2],
            "email": r[3]
        }
        for r in rows
    ]