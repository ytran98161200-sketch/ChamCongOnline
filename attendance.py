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
                SELECT
                    id,
                    check_in
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
        logs = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM attendance_logs
            WHERE employee_code=:employee_code
            AND DATE(scan_time)=CURRENT_DATE
            """),
            {
                "employee_code": employee_code
            }
        ).scalar()
        if logs <= 1:
            return False
            conn.execute(
                text("""
                UPDATE attendance
                SET
                    check_out = (
                        SELECT MAX(scan_time)
                        FROM attendance_logs
                        WHERE employee_code=:employee_code
                        AND DATE(scan_time)=CURRENT_DATE
                    ),

                    work_hours =
                        ROUND(
                            (
                                EXTRACT(
                                    EPOCH FROM (
                                        SELECT MAX(scan_time)
                                        FROM attendance_logs
                                        WHERE employee_code=:employee_code
                                        AND DATE(scan_time)=CURRENT_DATE
                                    ) - check_in
                                ) / 3600
                            )::numeric,
                            2
                        ),

                    workday =
                        CASE
                            WHEN
                                EXTRACT(
                                    EPOCH FROM (
                                        NOW() - check_in
                                    )
                                ) / 3600 >= 6
                            THEN 1
                            ELSE 0
                        END

                WHERE id=:id
                """),
                {
                    {
                        "id": row.id,
                        "employee_code": employee_code
                    }
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
                    check_in,
                    check_out,
                    work_hours,
                    workday
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
            "Check Out",
            "Số giờ",
            "Công",
            
        ]
    )