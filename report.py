from database import engine
from sqlalchemy import text
import pandas as pd


def attendance_report(
    filter_type="today",
    selected_date=None,
    company_id=None,
    employee_type=None,
    employee_code=None
):

    condition = ""

    if filter_type == "today":
        condition = """
        DATE(a.scan_time)=CURRENT_DATE
        """

    elif filter_type == "yesterday":
        condition = """
        DATE(a.scan_time)=CURRENT_DATE - INTERVAL '1 day'
        """

    elif filter_type == "7days":
        condition = """
        DATE(a.scan_time)>=CURRENT_DATE - INTERVAL '7 day'
        """

    elif filter_type == "30days":
        condition = """
        DATE(a.scan_time)>=CURRENT_DATE - INTERVAL '30 day'
        """

    elif filter_type == "this_month":
        condition = """
        DATE_TRUNC('month',a.scan_time)
        =
        DATE_TRUNC('month',CURRENT_DATE)
        """

    elif filter_type == "last_month":
        condition = """
        DATE_TRUNC('month',a.scan_time)
        =
        DATE_TRUNC('month',CURRENT_DATE - INTERVAL '1 month')
        """

    elif filter_type == "custom":

        condition = """
        DATE(a.scan_time)=:selected_date
        """

    else:

        condition = "1=1"

    query = f"""
    SELECT

        a.employee_code,

        e.fullname,

        DATE(a.scan_time) AS work_date,

        MIN(a.scan_time) AS check_in,

        MAX(a.scan_time) AS check_out,

        ROUND(
            (
                EXTRACT(
                    EPOCH FROM
                    (
                        MAX(a.scan_time)
                        -
                        MIN(a.scan_time)
                    )
                ) / 3600
            )::numeric,
            2
        ) AS work_hours,

        CASE

            WHEN

                EXTRACT(
                    EPOCH FROM
                    (
                        MAX(a.scan_time)
                        -
                        MIN(a.scan_time)
                    )
                ) / 3600 >= 6

            THEN 1

            ELSE 0

        END AS workday

    FROM attendance_logs a

    LEFT JOIN employees e

        ON a.employee_code = e.employee_code

    WHERE

        {condition}

        AND
        (
            :company_id IS NULL
            OR e.company_id = :company_id
        )

        AND
        (
            :employee_type IS NULL
            OR e.employee_type = :employee_type
        )

        AND
        (
            :employee_code IS NULL
            OR e.employee_code = :employee_code
        )

    GROUP BY

        a.employee_code,

        e.fullname,

        DATE(a.scan_time)

    ORDER BY

        DATE(a.scan_time) DESC,

        a.employee_code
    """

    params = {

        "selected_date": selected_date,

        "company_id": company_id,

        "employee_type": employee_type,

        "employee_code": employee_code

    }

    with engine.connect() as conn:

        rows = conn.execute(
            text(query),
            params
        ).fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Họ tên",
            "Ngày",
            "Check In",
            "Check Out",
            "Số giờ",
            "Công"
        ]
    )


def get_total_workday():

    query = """
    SELECT

        employee_code,

        SUM(workday) AS total_workday

    FROM

    (

        SELECT

            employee_code,

            DATE(scan_time) AS work_date,

            CASE

                WHEN

                    EXTRACT(
                        EPOCH FROM
                        (
                            MAX(scan_time)
                            -
                            MIN(scan_time)
                        )
                    ) / 3600 >= 6

                THEN 1

                ELSE 0

            END AS workday

        FROM attendance_logs

        GROUP BY

            employee_code,

            DATE(scan_time)

    ) t

    GROUP BY employee_code

    ORDER BY employee_code
    """

    with engine.connect() as conn:

        rows = conn.execute(
            text(query)
        ).fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Tổng công"
        ]
    )