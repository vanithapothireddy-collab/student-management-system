import oracledb

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\Vanitha\Downloads\instantclient-basic-windows.x64-23.26.2.0.0 (1)\instantclient_23_0"
)

print("DB.PY LOADED")
print("THICK MODE:", not oracledb.is_thin_mode())

def get_connection():
    return oracledb.connect(
        user="VANITHA",
        password="pass123",
        dsn="localhost:1521/XE"
    )