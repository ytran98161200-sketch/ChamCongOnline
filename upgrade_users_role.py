from database import engine
from sqlalchemy import text

with engine.connect() as conn:

    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS employee_code VARCHAR(20)
    """))

    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS department VARCHAR(100)
    """))

    conn.execute(text("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
    """))

    conn.commit()

print("users upgraded")