from database import engine
from sqlalchemy import text
import pandas as pd


def add_shift(
    shift_code,
    shift_name,
    start_time,
    end_time,
    standard_workday,
    late_allow_minutes,
    early_allow_minutes
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO shifts(
                shift_code,
                shift_name,
                start_time,
                end_time,
                standard_workday,
                late_allow_minutes,
                early_allow_minutes
            )
            VALUES(
                :shift_code,
                :shift_name,
                :start_time,
                :end_time,
                :standard_workday,
                :late_allow_minutes,
                :early_allow_minutes
            )
            """),
            {
                "shift_code": shift_code,
                "shift_name": shift_name,
                "start_time": start_time,
                "end_time": end_time,
                "standard_workday": standard_workday,
                "late_allow_minutes": late_allow_minutes,
                "early_allow_minutes": early_allow_minutes
            }
        )

        conn.commit()


def get_shifts():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                shift_code,
                shift_name,
                start_time,
                end_time,
                standard_workday
            FROM shifts
            ORDER BY shift_code
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã Ca",
            "Tên Ca",
            "Giờ Vào",
            "Giờ Ra",
            "Công Chuẩn"
        ]
    )
def get_shift_codes():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT shift_code
            FROM shifts
            ORDER BY shift_code
            """)
        )

        rows = result.fetchall()

    return [r[0] for r in rows]

def get_shift_count():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM shifts
            """)
        )

        return result.scalar()