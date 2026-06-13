from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(
        text("""
        DELETE FROM attendance_logs
        """)
    )

    conn.commit()

print("logs cleared")