from database import engine
from sqlalchemy import text


def get_departments():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT department_name
            FROM departments
            ORDER BY department_name
            """)
        )

        rows = result.fetchall()

    return [r[0] for r in rows]


def add_department(
    department_name
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO departments(
                department_name
            )
            VALUES(
                :department_name
            )
            """),
            {
                "department_name": department_name
            }
        )

        conn.commit()