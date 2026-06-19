import oracledb

oracledb.init_oracle_client(
    lib_dir=r"C:\Users\Vanitha\Downloads\instantclient-basic-windows.x64-23.26.2.0.0 (1)\instantclient_23_0"
)

print("Thick mode:", not oracledb.is_thin_mode())

conn = oracledb.connect(
    user="VANITHA",
    password="pass123",
    dsn="localhost:1521/XE"
)

print("CONNECTED")
conn.close()
