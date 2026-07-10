from fastapi import APIRouter, HTTPException
from db import get_connection
from models.student import StudentCreate
from logger_config import logger
from utils.audit import save_audit

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get("/")
def get_students(

    page: int = 1,
    page_size: int = 10,
    sort_by: str = "student_id",
    sort_order: str = "ASC"

):

    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size

    allowed_columns = {

        "student_id": "s.student_id",
        "student_name": "s.student_name",
        "gender": "s.gender",
        "department_name": "d.department_name",
        "batch_name": "b.batch_name"

    }

    column = allowed_columns.get(sort_by, "s.student_id")

    order = "DESC" if sort_order.upper() == "DESC" else "ASC"

    sql = f"""

        SELECT
            student_id,
            student_name,
            gender,
            department_name,
            batch_name
        FROM
        (
            SELECT
                s.student_id,
                s.student_name,
                s.gender,
                d.department_name,
                b.batch_name,
                ROW_NUMBER() OVER(
                    ORDER BY {column} {order}
                ) rn

            FROM students s

            LEFT JOIN departments d
                ON s.department_id = d.department_id

            LEFT JOIN batches b
                ON s.batch_id = b.batch_id

            WHERE s.is_active='Y'
        )

        WHERE rn BETWEEN :1 AND :2

    """

    cursor.execute(

        sql,

        (

            offset + 1,
            offset + page_size

        )

    )

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_name": row[3],
            "batch_name": row[4]

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

    cursor.execute("""

        SELECT student_seq.CURRVAL
        FROM dual

    """)

    student_id = cursor.fetchone()[0]

    save_audit(

        "STUDENTS",
        "INSERT",
        student_id

    )

    cursor.close()
    conn.close()

    return {

        "message": "Student Created Successfully"

    }



@router.get("/search/")
def search_student(

    name: str = "",
    gender: str = "",
    department: str = "",
    batch: str = ""

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            s.student_id,
            s.student_name,
            s.gender,
            d.department_name,
            b.batch_name

        FROM students s

        LEFT JOIN departments d
            ON s.department_id=d.department_id

        LEFT JOIN batches b
            ON s.batch_id=b.batch_id

        WHERE

            UPPER(s.student_name)
                LIKE UPPER(:1)

        AND

            UPPER(NVL(s.gender,''))
                LIKE UPPER(:2)

        AND

            UPPER(NVL(d.department_name,''))
                LIKE UPPER(:3)

        AND

            UPPER(NVL(b.batch_name,''))
                LIKE UPPER(:4)

        AND s.is_active='Y'

        ORDER BY s.student_id

    """,

    (

        f"%{name}%",
        f"%{gender}%",
        f"%{department}%",
        f"%{batch}%"

    ))

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "student_id": row[0],
            "student_name": row[1],
            "gender": row[2],
            "department_name": row[3],
            "batch_name": row[4]

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
            NVL(f.status,'Pending')

        FROM students s

        LEFT JOIN departments d
            ON s.department_id = d.department_id

        LEFT JOIN fees f
            ON s.student_id = f.student_id

        WHERE s.is_active = 'Y'

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
        WHERE is_active='Y'

    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {

        "total_students": count

    }



@router.get("/{student_id}")
def get_student(student_id: int):

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

        WHERE student_id=:1
        AND is_active='Y'

    """, (student_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:

        raise HTTPException(

            status_code=404,
            detail="Student Not Found"

        )

    return {

        "student_id": row[0],
        "student_name": row[1],
        "gender": row[2],
        "department_id": row[3],
        "batch_id": row[4]

    }




@router.put("/{student_id}")
def update_student(student_id: int, student: StudentCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE students

        SET

            student_name=:1,
            gender=:2,
            department_id=:3,
            batch_id=:4

        WHERE student_id=:5

    """,

    (

        student.student_name,
        student.gender,
        student.department_id,
        student.batch_id,
        student_id

    ))

    conn.commit()

    save_audit(

        "STUDENTS",
        "UPDATE",
        student_id

    )

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

        UPDATE students

        SET is_active='N'

        WHERE student_id=:1

    """, (student_id,))

    conn.commit()

    save_audit(

        "STUDENTS",
        "DELETE",
        student_id

    )

    cursor.close()
    conn.close()

    return {

        "message": "Student Deleted Successfully"

    }