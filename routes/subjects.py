from fastapi import APIRouter, HTTPException
from db import get_connection
from models.subject import SubjectCreate
from utils.audit import save_audit
router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

# ---------------- GET ALL ----------------

@router.get("/")
def get_subjects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            subject_id,
            subject_name
        FROM subjects
        ORDER BY subject_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "subject_id": row[0],
            "subject_name": row[1]
        })

    cursor.close()
    conn.close()

    return result


# ---------------- GET ONE ----------------

@router.get("/{subject_id}")
def get_subject(subject_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            subject_id,
            subject_name
        FROM subjects
        WHERE subject_id = :1
    """, (subject_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    return {
        "subject_id": row[0],
        "subject_name": row[1]
    }


# ---------------- CREATE ----------------

@router.post("/")
def create_subject(subject: SubjectCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (
            subject_id,
            subject_name
        )
        VALUES
        (
            SUBJECT_SEQ.NEXTVAL,
            :1
        )
    """, (
        subject.subject_name,
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Subject Created Successfully"
    }


# ---------------- UPDATE ----------------
@router.post("/")
def create_subject(subject: SubjectCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subjects
        (
            subject_id,
            subject_name,
            is_active
        )
        VALUES
        (
            SUBJECT_SEQ.NEXTVAL,
            :1,
            'Y'
        )
    """,
    (
        subject.subject_name,
    ))

    conn.commit()

    cursor.execute(
        "SELECT SUBJECT_SEQ.CURRVAL FROM dual"
    )

    subject_id = cursor.fetchone()[0]

    save_audit(
        "SUBJECTS",
        "INSERT",
        subject_id
    )

    cursor.close()
    conn.close()

    return {
        "message": "Subject Created Successfully"
    }
# ---------------- DELETE ----------------
@router.delete("/{subject_id}")
def delete_subject(subject_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subjects
        SET
            is_active='N'
        WHERE
            subject_id=:1
    """,
    (
        subject_id,
    ))

    conn.commit()

    save_audit(
        "SUBJECTS",
        "DELETE",
        subject_id
    )

    cursor.close()
    conn.close()

    return {
        "message": "Subject Deleted Successfully"
    }