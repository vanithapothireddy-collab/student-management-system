from fastapi import APIRouter, HTTPException
from db import get_connection
from models.department import DepartmentCreate
from fastapi import status
import traceback
from utils.audit import save_audit
from fastapi import APIRouter

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)
@router.get("/")
def get_departments(

    page: int = 1,
    page_size: int = 10,
    sort_by: str = "department_id",
    sort_order: str = "ASC"

):

    conn = get_connection()
    cursor = conn.cursor()

    offset = (page - 1) * page_size

    allowed_columns = {

        "department_id": "department_id",
        "department_name": "department_name"

    }

    column = allowed_columns.get(
        sort_by,
        "department_id"
    )

    order = "DESC" if sort_order.upper() == "DESC" else "ASC"

    sql = f"""

        SELECT
            department_id,
            department_name
        FROM
        (
            SELECT
                department_id,
                department_name,
                ROW_NUMBER() OVER
                (
                    ORDER BY {column} {order}
                ) rn
            FROM departments
            WHERE is_active='Y'
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

            "department_id": row[0],
            "department_name": row[1]

        })

    cursor.close()
    conn.close()

    return result
# ==========================================
# Create Department
# ==========================================

@router.post("/")
def create_department(department: DepartmentCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO departments
        (

            department_id,
            department_name,
            is_active

        )

        VALUES
        (

            dept_seq.NEXTVAL,
            :1,
            'Y'

        )

    """,

    (

        department.department_name,

    )

    )

    conn.commit()

    # Get newly created Department ID
    cursor.execute("""

        SELECT dept_seq.CURRVAL

        FROM dual

    """)

    department_id = cursor.fetchone()[0]

    # Save Audit Log
    save_audit(

        "DEPARTMENTS",

        "INSERT",

        department_id

    )

    cursor.close()
    conn.close()

    return {

        "message": "Department Created Successfully"

    }# ==========================================
# Get Department By ID
# ==========================================

@router.get("/{department_id}")
def get_department(department_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            department_id,
            department_name

        FROM departments

        WHERE

            department_id = :1

        AND

            is_active = 'Y'

    """,

    (

        department_id,

    )

    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:

        return {

            "message": "Department Not Found"

        }

    return {

        "department_id": row[0],
        "department_name": row[1]

    }
@router.get("/search/")
def search_departments(

    name: str = ""

):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            department_id,
            department_name

        FROM departments

        WHERE

            is_active = 'Y'

        AND

            UPPER(department_name)

            LIKE

            UPPER(:1)

        ORDER BY department_name

    """,

    (

        f"%{name}%",

    )

    )

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "department_id": row[0],

            "department_name": row[1]

        })

    cursor.close()
    conn.close()

    return result
# ==========================================
# Update Department
# ==========================================

@router.put("/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentCreate
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE departments

        SET

            department_name = :1

        WHERE

            department_id = :2

        AND

            is_active = 'Y'

    """,

    (

        department.department_name,
        department_id

    )

    )

    conn.commit()

    # Save Audit Log
    save_audit(

        "DEPARTMENTS",

        "UPDATE",

        department_id

    )

    cursor.close()
    conn.close()

    return {

        "message": "Department Updated Successfully"

    }# ==========================================
# Soft Delete Department
# ==========================================

@router.delete("/{department_id}")
def delete_department(department_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        UPDATE departments

        SET

            is_active = 'N'

        WHERE

            department_id = :1

    """,

    (

        department_id,

    )

    )

    conn.commit()

    # Audit Log

    save_audit(

        "DEPARTMENTS",

        "DELETE",

        department_id

    )

    cursor.close()
    conn.close()

    return {

        "message": "Department Deleted Successfully"

    }