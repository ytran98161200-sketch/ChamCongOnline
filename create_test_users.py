from database import engine
from sqlalchemy import text
import bcrypt

users = [
    {
        "username": "admin",
        "password": "123456",
        "role": "admin",
        "employee_code": None,
        "department": "SYSTEM"
    },
    {
        "username": "cuong.tp",
        "password": "123456",
        "role": "manager",
        "employee_code": "TP001",
        "department": "HCNS"
    },
    {
        "username": "NV001",
        "password": "123456",
        "role": "employee",
        "employee_code": "NV001",
        "department": "HCNS"
    },
    {
        "username": "NV002",
        "password": "123456",
        "role": "employee",
        "employee_code": "NV002",
        "department": "HCNS"
    },
    {
        "username": "NV003",
        "password": "123456",
        "role": "employee",
        "employee_code": "NV003",
        "department": "HCNS"
    },
    {
        "username": "NV004",
        "password": "123456",
        "role": "employee",
        "employee_code": "NV004",
        "department": "HCNS"
    },
    {
        "username": "NV005",
        "password": "123456",
        "role": "employee",
        "employee_code": "NV005",
        "department": "HCNS"
    }
]

with engine.connect() as conn:

    for user in users:

        password_hash = bcrypt.hashpw(
            user["password"].encode(),
            bcrypt.gensalt()
        ).decode()

        conn.execute(
            text("""
            INSERT INTO users(
                username,
                password_hash,
                role,
                employee_code,
                department
            )
            VALUES(
                :username,
                :password_hash,
                :role,
                :employee_code,
                :department
            )
            ON CONFLICT (username)
            DO NOTHING
            """),
            {
                "username": user["username"],
                "password_hash": password_hash,
                "role": user["role"],
                "employee_code": user["employee_code"],
                "department": user["department"]
            }
        )

    conn.commit()

print("Tạo tài khoản thành công")