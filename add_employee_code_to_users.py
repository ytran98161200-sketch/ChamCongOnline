from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(
        text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS employee_code VARCHAR(20)
        """)
    )

    conn.commit()

print("employee_code added")