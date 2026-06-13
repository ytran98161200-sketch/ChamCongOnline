from database import engine
from sqlalchemy import text
import bcrypt

username = "NV001"
password = "123456"

password_hash = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
).decode()

with engine.connect() as conn:

    conn.execute(
        text("""
        INSERT INTO users(
            username,
            password_hash,
            role,
            employee_code
        )
        VALUES(
            :username,
            :password_hash,
            'employee',
            'NV001'
        )
        """),
        {
            "username": username,
            "password_hash": password_hash
        }
    )

    conn.commit()

print("Employee user created")