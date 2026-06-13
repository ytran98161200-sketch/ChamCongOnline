from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(
        text("""
        ALTER TABLE attendance_logs
        ADD COLUMN IF NOT EXISTS note TEXT
        """)
    )

    conn.commit()

print("note column added")