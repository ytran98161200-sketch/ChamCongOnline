from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    result = conn.execute(
        text("""
        SELECT username, role, employee_code
        FROM users
        """)
    )

    for row in result:
        print(row)