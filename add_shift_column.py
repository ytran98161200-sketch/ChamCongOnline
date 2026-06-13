from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(
        text("""
        ALTER TABLE employees
        ADD COLUMN IF NOT EXISTS shift_code VARCHAR(50)
        """)
    )

    conn.commit()

print("Shift column added")