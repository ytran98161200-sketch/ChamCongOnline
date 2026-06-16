from database import engine
from sqlalchemy import text
import pandas as pd


def create_request(
    employee_code,
    request_date,
    check_in,
    check_out,
    reason
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO attendance_requests(
                employee_code,
                request_date,
                check_in,
                check_out,
                reason
            )
            VALUES(
                :employee_code,
                :request_date,
                :check_in,
                :check_out,
                :reason
            )
            """),
            {
                "employee_code": employee_code,
                "request_date": request_date,
                "check_in": check_in,
                "check_out": check_out,
                "reason": reason
            }
        )

        conn.commit()