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
                u.username,
                e.fullname,
                e.department,
                u.role,
                u.employee_code,
                u.is_active
            FROM users u
            LEFT JOIN employees e
                ON u.employee_code = e.employee_code
            ORDER BY u.username
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "username",
            "fullname",
            "department",
            "role",
            "employee_code",
            "is_active"
        ]
    )
def get_user(username):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM users
            WHERE username=:username
            """),
            {
                "username": username
            }
        )

        row = result.fetchone()

    if row:
        return dict(row._mapping)

    return None
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
        
def update_user(
    username,
    role,
    is_active
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE users
            SET
                role=:role,
                is_active=:is_active
            WHERE username=:username
            """),
            {
                "username": username,
                "role": role,
                "is_active": is_active
            }
        )

        conn.commit()

def change_password(
    username,
    old_password,
    new_password
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT password_hash
            FROM users
            WHERE username=:username
            """),
            {
                "username": username
            }
        )

        row = result.fetchone()

        if not row:
            return False

        if not bcrypt.checkpw(
            old_password.encode(),
            row[0].encode()
        ):
            return False

        password_hash = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()

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

        return True