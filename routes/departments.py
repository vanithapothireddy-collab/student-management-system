from fastapi import APIRouter, HTTPException
from db import get_connection
from models.department import DepartmentCreate
from fastapi import status
import traceback

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)

@router.get("/")
def get_departments():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT department_id,
                   department_name
            FROM departments
            ORDER BY department_name
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/")
def create_department(department: DepartmentCreate):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Check for duplicate department
        cursor.execute("""
            SELECT COUNT(*)
            FROM departments
            WHERE UPPER(department_name)=UPPER(:1)
        """, (
            department.department_name,
        ))

        count = cursor.fetchone()[0]

        if count > 0:
            raise HTTPException(
                status_code=400,
                detail="Department already exists."
            )

        # Insert department
        cursor.execute("""
            INSERT INTO departments
            (
                department_id,
                department_name
            )
            VALUES
            (
                DEPT_SEQ.NEXTVAL,
                :1
            )
        """, (
            department.department_name,
        ))

        conn.commit()

        return {
             "status": status.HTTP_201_CREATED,
            "message": "Department created successfully"
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:

        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        cursor.close()
        conn.close()
@router.get("/{department_id}")
def get_department(department_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT department_id,
               department_name
        FROM departments
        WHERE department_id = :1
    """, (department_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return {
        "department_id": row[0],
        "department_name": row[1]
    }
@router.put("/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentCreate
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM departments
            WHERE department_id = :1
        """, (department_id,))

        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        cursor.execute("""
            UPDATE departments
            SET department_name = :1
            WHERE department_id = :2
        """, (
            department.department_name,
            department_id
        ))

        conn.commit()

        return {
            "message": "Department updated successfully"
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()
@router.delete("/{department_id}")
def delete_department(department_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM departments
            WHERE department_id = :1
        """, (department_id,))

        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        cursor.execute("""
            DELETE FROM departments
            WHERE department_id = :1
        """, (department_id,))

        conn.commit()

        return {
            "message": "Department deleted successfully"
        }

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        cursor.close()
        conn.close()