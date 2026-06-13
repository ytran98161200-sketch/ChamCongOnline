from database import engine
from sqlalchemy import text
import pandas as pd


def check_in(employee_code):

    with engine.connect() as conn:

        existed = conn.execute(
            text("""
            SELECT id
            FROM attendance
            WHERE employee_code=:employee_code
            AND work_date=CURRENT_DATE
            """),
            {
                "employee_code": employee_code
            }
        ).fetchone()

        if existed:
            return False

        conn.execute(
            text("""
            INSERT INTO attendance(
                employee_code,
                work_date,
                check_in
            )
            VALUES(
                :employee_code,
                CURRENT_DATE,
                NOW()
            )
            """),
            {
                "employee_code": employee_code
            }
        )

        conn.commit()

    return True


def check_out(employee_code):

    with engine.connect() as conn:

        row = conn.execute(
            text("""
            SELECT id
            FROM attendance
            WHERE employee_code=:employee_code
            AND work_date=CURRENT_DATE
            """),
            {
                "employee_code": employee_code
            }
        ).fetchone()

        if not row:
            return False

        conn.execute(
            text("""
            UPDATE attendance
            SET check_out=NOW()
            WHERE id=:id
            """),
            {
                "id": row.id
            }
        )

        conn.commit()

    return True


def get_attendance():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                employee_code,
                work_date,
                checkin,
                checkout
            FROM attendance
            ORDER BY id DESC
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Ngày",
            "Check In",
            "Check Out"
        ]
    )