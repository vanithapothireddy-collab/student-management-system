import os
import oracledb

print("DB.PY LOADED")
print("THIN MODE:", oracledb.is_thin_mode())

def get_connection():
    return oracledb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dsn=os.getenv("DB_DSN")
    )