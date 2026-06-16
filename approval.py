from database import engine
from sqlalchemy import text

def get_department_manager(department):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                employee_code,
                fullname
            FROM employees
            WHERE department=:department
            AND position='Trưởng phòng'
            LIMIT 1
            """),
            {
                "department": department
            }
        )

        row = result.fetchone()

    if row:
        return {
            "employee_code": row[0],
            "fullname": row[1]
        }

    return None