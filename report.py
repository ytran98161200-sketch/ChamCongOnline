from database import engine
from sqlalchemy import text
import pandas as pd


def attendance_report():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                a.employee_code,
                e.fullname,
                a.scan_time,
                a.note
            FROM attendance_logs a

            LEFT JOIN employees e
                ON a.employee_code=e.employee_code

            ORDER BY a.scan_time DESC
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Họ tên",
            "Thời gian",
            "Ghi chú"
        ]
    )