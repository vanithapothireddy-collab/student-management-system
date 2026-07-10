from fastapi import APIRouter, HTTPException
from db import get_connection
from models.fees import FeeCreate

router = APIRouter(
    prefix="/fees",
    tags=["Fees"]
)

# ----------------------------
# GET ALL FEES
# ----------------------------

@router.get("/")
def get_fees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.fee_id,
            s.student_name,
            f.student_id,
            f.total_fee,
            f.paid_fee,
            f.status
        FROM fees f
        JOIN students s
            ON f.student_id = s.student_id
        ORDER BY f.fee_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "fee_id": row[0],

            "student_name": row[1],

            "student_id": row[2],

            "total_fee": row[3],

            "paid_fee": row[4],

            "pending_fee": row[3] - row[4],

            "status": row[5]

        })

    cursor.close()
    conn.close()

    return result


# ----------------------------
# GET ONE
# ----------------------------
# ----------------------------
# CREATE
# ----------------------------

@router.post("/")
def create_fee(fee: FeeCreate):

    if fee.paid_fee > fee.total_fee:
        raise HTTPException(
            status_code=400,
            detail="Paid fee cannot be greater than Total fee."
        )

    status = "PAID" if fee.paid_fee >= fee.total_fee else "PARTIAL"
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fees
        (
            fee_id,
            student_id,
            total_fee,
            paid_fee,
            status
        )
        VALUES
        (
            fee_seq.NEXTVAL,
            :1,
            :2,
            :3,
            :4
        )
    """, (
        fee.student_id,
        fee.total_fee,
        fee.paid_fee,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Fee Added Successfully"}

# ----------------------------
# UPDATE
# ----------------------------
@router.put("/{fee_id}")
def update_fee(fee_id: int, fee: FeeCreate):
    print("Fee ID:", fee_id)
    print("Current Payment Entered:", fee.paid_fee)

    conn = get_connection()
    cursor = conn.cursor()

    # Get current fee details
    cursor.execute("""
        SELECT total_fee, paid_fee
        FROM fees
        WHERE fee_id=:1
    """, (fee_id,))

    row = cursor.fetchone()

    if row is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Fee Record Not Found")

    total_fee = row[0]
    current_paid = row[1]

    new_paid = current_paid + fee.paid_fee

    # Prevent overpayment
    if new_paid > total_fee:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Payment exceeds pending amount. Pending = {total_fee-current_paid}"
        )

    status = "PAID" if new_paid >= total_fee else "PARTIAL"
    cursor.execute("""
        UPDATE fees
        SET
            paid_fee=:1,
            status=:2
        WHERE fee_id=:3
    """, (
        new_paid,
        status,
        fee_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Payment Updated Successfully"
    }

# ----------------------------
# DELETE
# ----------------------------

@router.delete("/{fee_id}")
def delete_fee(fee_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        DELETE FROM fees

        WHERE fee_id=:1

    """, (fee_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {

        "message": "Fee Deleted Successfully"

    }


# ----------------------------
# SEARCH
# ----------------------------

@router.get("/search/{student_name}")
def search_fee(student_name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            f.fee_id,

            s.student_name,

            f.student_id,

            f.total_fee,

            f.paid_fee,

            f.status

        FROM fees f

        JOIN students s

            ON f.student_id=s.student_id

        WHERE UPPER(s.student_name)

        LIKE UPPER(:1)

        ORDER BY f.fee_id

    """, ('%' + student_name + '%',))

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "fee_id": row[0],

            "student_name": row[1],

            "student_id": row[2],

            "total_fee": row[3],

            "paid_fee": row[4],

            "pending_fee": row[3] - row[4],

            "status": row[5]

        })

    cursor.close()
    conn.close()

    return result
# ----------------------------
# TOTAL COLLECTION
# ----------------------------

@router.get("/dashboard/total-collection")
def total_collection():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT NVL(SUM(paid_fee),0)
        FROM fees
    """)

    amount = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "total_collection": amount
    }


# ----------------------------
# PENDING COLLECTION
# ----------------------------

@router.get("/dashboard/pending-collection")
def pending_collection():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT NVL(SUM(total_fee - paid_fee),0)
        FROM fees
    """)

    amount = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "pending_collection": amount
    }


# ----------------------------
# PAID STUDENTS
# ----------------------------

@router.get("/dashboard/paid-students")
def paid_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM fees
        WHERE UPPER(status)='PAID'
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "paid_students": count
    }


# ----------------------------
# PENDING STUDENTS
# ----------------------------

@router.get("/dashboard/pending-students")
def pending_students():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM fees
        WHERE UPPER(status)='PARTIAL'
    """)

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "pending_students": count
    }
# ----------------------------
# FEE STATISTICS
# ----------------------------

@router.get("/statistics")
def fee_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            NVL(SUM(total_fee),0),
            NVL(SUM(paid_fee),0),
            NVL(SUM(total_fee-paid_fee),0)
        FROM fees
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return {

        "total_fee": row[0],

        "paid_fee": row[1],

        "pending_fee": row[2]

    }
# ----------------------------
# PAYMENT REPORT
# ----------------------------

@router.get("/payment-report")
def payment_report():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_name,
            f.total_fee,
            f.paid_fee,
            (f.total_fee - f.paid_fee) pending_fee,
            f.status
        FROM fees f
        JOIN students s
            ON f.student_id = s.student_id
        ORDER BY s.student_name
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:

        result.append({

            "student_name": row[0],

            "total_fee": row[1],

            "paid_fee": row[2],

            "pending_fee": row[3],

            "status": row[4]

        })

    cursor.close()
    conn.close()

    return result

@router.get("/{fee_id}")
def get_fee(fee_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            fee_id,

            student_id,

            total_fee,

            paid_fee,

            status

        FROM fees

        WHERE fee_id=:1

    """, (fee_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:

        raise HTTPException(

            status_code=404,

            detail="Fee Record Not Found"

        )

    return {

        "fee_id": row[0],

        "student_id": row[1],

        "total_fee": row[2],

        "paid_fee": row[3],

        "status": row[4]

    }


