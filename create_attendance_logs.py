from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(
        text("""
        CREATE TABLE IF NOT EXISTS attendance_logs (

            id SERIAL PRIMARY KEY,

            employee_code VARCHAR(20),

            scan_time TIMESTAMP DEFAULT NOW()

        )
        """)
    )

    conn.commit()

print("attendance_logs created")