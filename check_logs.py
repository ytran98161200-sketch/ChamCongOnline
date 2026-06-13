from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    result = conn.execute(
        text("""
        SELECT *
        FROM attendance_logs
        ORDER BY id DESC
        LIMIT 5
        """)
    )

    for row in result:
        print(row)