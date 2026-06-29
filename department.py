from database import engine
from sqlalchemy import text


# ==========================
# LẤY DANH SÁCH PHÒNG BAN
# ==========================
def get_departments(company_id=None):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT
                    id,
                    department_name
                FROM departments
                WHERE
                    (:company_id IS NULL OR company_id=:company_id)
                ORDER BY department_name
            """),
            {
                "company_id": company_id
            }
        )

        rows = result.fetchall()

    return [
        {
            "id": row[0],
            "department_name": row[1]
        }
        for row in rows
    ]


# ==========================
# THÊM PHÒNG BAN
# ==========================
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