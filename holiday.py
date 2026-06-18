from database import engine
from sqlalchemy import text
import pandas as pd


def add_holiday(
    holiday_date,
    holiday_name
):

    with engine.begin() as conn:

        conn.execute(
            text("""
            INSERT INTO holidays(
                holiday_date,
                holiday_name
            )
            VALUES(
                :holiday_date,
                :holiday_name
            )
            """),
            {
                "holiday_date": holiday_date,
                "holiday_name": holiday_name
            }
        )


def get_holidays():

    with engine.connect() as conn:

        rows = conn.execute(
            text("""
            SELECT
                holiday_date,
                holiday_name
            FROM holidays
            ORDER BY holiday_date
            """)
        ).fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Ngày",
            "Tên ngày lễ"
        ]
    )
    
from sqlalchemy import text


def get_holiday_dict():

    with engine.connect() as conn:

        rows = conn.execute(
            text("""
            SELECT
                holiday_date,
                holiday_name
            FROM holidays
            """)
        ).fetchall()

    data = {}

    for row in rows:

        data[str(row[0])] = row[1]

    return data