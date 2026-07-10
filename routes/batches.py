from fastapi import APIRouter, HTTPException
from db import get_connection
from models.batch import BatchCreate

router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)

@router.get("/")
def get_batches():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            batch_id,
            batch_name,
            year
        FROM batches
        ORDER BY batch_id
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "batch_id": row[0],
            "batch_name": row[1],
            "year": row[2]
        })

    cursor.close()
    conn.close()

    return result


@router.post("/")
def create_batch(batch: BatchCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO batches
        (
            batch_id,
            batch_name,
            year
        )
        VALUES
        (
            batch_seq.NEXTVAL,
            :1,
            :2
        )
    """,
    (
        batch.batch_name,
        batch.year
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Batch Created Successfully"
    }


@router.get("/{batch_id}")
def get_batch(batch_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            batch_id,
            batch_name,
            year
        FROM batches
        WHERE batch_id = :1
    """, (batch_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Batch Not Found"
        )

    return {
        "batch_id": row[0],
        "batch_name": row[1],
        "year": row[2]
    }


@router.put("/{batch_id}")
def update_batch(batch_id: int, batch: BatchCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE batches
        SET
            batch_name = :1,
            year = :2
        WHERE batch_id = :3
    """,
    (
        batch.batch_name,
        batch.year,
        batch_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Batch Updated Successfully"
    }


@router.delete("/{batch_id}")
def delete_batch(batch_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM batches
        WHERE batch_id = :1
    """, (batch_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Batch Deleted Successfully"
    }