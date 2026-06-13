from database import engine
from sqlalchemy import text
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

def add_log(employee_code, note=""):

    vietnam_time = datetime.now()

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO attendance_logs(
                employee_code,
                scan_time,
                note
            )
            VALUES(
                :employee_code,
                :scan_time,
                :note
            )
            """),
            {
                "employee_code": employee_code,
                "scan_time": vietnam_time,
                "note": note
            }
        )
        print("GIỜ VN:", vietnam_time)
        conn.commit()

def get_today_logs(employee_code):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT scan_time
            FROM attendance_logs
            WHERE employee_code=:employee_code
            AND DATE(scan_time)=CURRENT_DATE
            ORDER BY scan_time
            """),
            {
                "employee_code": employee_code
            }
        )

        return result.fetchall()
    
import pandas as pd

def get_all_logs():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                a.scan_time,
                a.employee_code,
                e.fullname,
                COALESCE(a.note,'')
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
            "Thời gian",
            "Mã NV",
            "Họ tên",
            "Ghi chú"
        ]
    )

def get_logs_by_date(selected_date, employee_code=None):

    with engine.connect() as conn:

        if employee_code and employee_code != "Tất cả":

            result = conn.execute(
                text("""
                SELECT
                    a.scan_time,
                    a.employee_code,
                    e.fullname,
                    COALESCE(a.note,'')

                FROM attendance_logs a

                LEFT JOIN employees e
                    ON a.employee_code=e.employee_code

                WHERE
                    DATE(a.scan_time)=:selected_date
                    AND a.employee_code=:employee_code

                ORDER BY a.scan_time DESC
                """),
                {
                    "selected_date": selected_date,
                    "employee_code": employee_code
                }
            )

        else:

            result = conn.execute(
                text("""
                SELECT
                    a.scan_time,
                    a.employee_code,
                    e.fullname,
                    COALESCE(a.note,'')

                FROM attendance_logs a

                LEFT JOIN employees e
                    ON a.employee_code=e.employee_code

                WHERE DATE(a.scan_time)=:selected_date

                ORDER BY a.scan_time DESC
                """),
                {
                    "selected_date": selected_date
                }
            )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Thời gian",
            "Mã NV",
            "Họ tên",
            "Ghi chú"
        ]
    )
    
def get_today_attendance_count():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT COUNT(DISTINCT employee_code)
            FROM attendance_logs
            WHERE DATE(scan_time)=CURRENT_DATE
            """)
        )

        return result.scalar() or 0

def get_today_note_count():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM attendance_logs
            WHERE DATE(scan_time)=CURRENT_DATE
            AND COALESCE(note,'') <> ''
            """)
        )

        return result.scalar() or 0
    
    
def get_today_attendance_employees():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT DISTINCT employee_code
            FROM attendance_logs
            WHERE DATE(scan_time)=CURRENT_DATE
            """)
        )

        rows = result.fetchall()

    return [r[0] for r in rows]

def get_daily_summary(selected_date):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                a.employee_code,
                e.fullname,
                a.scan_time

            FROM attendance_logs a

            LEFT JOIN employees e
                ON a.employee_code=e.employee_code

            WHERE DATE(a.scan_time)=:selected_date

            ORDER BY
                a.employee_code,
                a.scan_time
            """),
            {
                "selected_date": selected_date
            }
        )

        rows = result.fetchall()

    data = {}

    for employee_code, fullname, scan_time in rows:

        if employee_code not in data:

            data[employee_code] = {
                "fullname": fullname,
                "logs": []
            }

        data[employee_code]["logs"].append(
            scan_time.strftime("%H:%M")
        )

    summary = []

    for employee_code, info in data.items():

        logs = info["logs"]

        summary.append([
            employee_code,
            info["fullname"],
            logs[0] if len(logs) > 0 else "",
            logs[1] if len(logs) > 1 else "",
            logs[2] if len(logs) > 2 else "",
            logs[3] if len(logs) > 3 else ""
        ])

    return pd.DataFrame(
        summary,
        columns=[
            "Mã NV",
            "Họ tên",
            "Vào sáng",
            "Ra sáng",
            "Vào chiều",
            "Ra chiều"
        ]
    )