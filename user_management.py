from database import engine
from sqlalchemy import text
import bcrypt
import pandas as pd

def create_user(
    username,
    password,
    role,
    employee_code,
    managed_department=None
):

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
                employee_code,
                managed_department,
                is_active
            )
            VALUES(
                :username,
                :password_hash,
                :role,
                :employee_code,
                :managed_department,
                TRUE
            )
            """),
            {
                "username": username,
                "password_hash": password_hash,
                "role": role,
                "employee_code": employee_code,
                "managed_department": managed_department
            }
        )

        conn.commit()


def get_users():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                username,
                role,
                employee_code,
                is_active
            FROM users
            ORDER BY username
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "username",
            "role",
            "employee_code",
            "is_active"
        ]
    )
def reset_password(
    username,
    new_password
):

    import bcrypt

    password_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    ).decode()

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE users
            SET password_hash=:password_hash
            WHERE username=:username
            """),
            {
                "username": username,
                "password_hash": password_hash
            }
        )

        conn.commit()