from db import get_connection

def save_audit(

    table_name,

    action,

    record_id,

    username="Admin"

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO audit_log
        (
            log_id,
            table_name,
            action,
            record_id,
            action_date,
            username
        )

        VALUES
        (
            audit_seq.NEXTVAL,
            :1,
            :2,
            :3,
            SYSDATE,
            :4
        )

    """,

    (
        table_name,
        action,
        record_id,
        username
    ))

    conn.commit()

    cursor.close()

    conn.close()