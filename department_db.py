from sqlalchemy import text
from database import engine


def get_departments(company_id=None):

    sql = """
        SELECT
            id,
            department_name,
            company_id
        FROM departments
    """

    params = {}

    if company_id is not None:
        sql += """
            WHERE company_id=:company_id
        """
        params["company_id"] = company_id

    sql += """
        ORDER BY department_name
    """

    with engine.connect() as conn:

        rows = conn.execute(
            text(sql),
            params
        ).mappings().all()

    return rows


def add_department(
    company_id,
    department_name
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO departments(
                    company_id,
                    department_name
                )
                VALUES(
                    :company_id,
                    :department_name
                )
            """),
            {
                "company_id": company_id,
                "department_name": department_name
            }
        )


def update_department(
    department_id,
    company_id,
    department_name
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE departments
                SET
                    company_id=:company_id,
                    department_name=:department_name
                WHERE id=:department_id
            """),
            {
                "department_id": department_id,
                "company_id": company_id,
                "department_name": department_name
            }
        )


def delete_department(department_id):

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE FROM departments
                WHERE id=:department_id
            """),
            {
                "department_id": department_id
            }
        )