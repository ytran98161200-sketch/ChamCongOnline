from database import engine
from sqlalchemy import text
import bcrypt

password = bcrypt.hashpw(
    b"123456",
    bcrypt.gensalt()
).decode()

with engine.connect() as conn:

    conn.execute(
        text("""
        INSERT INTO users(
            username,
            password_hash,
            role
        )
        VALUES(
            'admin',
            :pwd,
            'admin'
        )
        ON CONFLICT(username)
        DO NOTHING
        """),
        {"pwd": password}
    )

    conn.commit()

print("Admin created")