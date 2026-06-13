from database import engine
from sqlalchemy import text

sql = """
CREATE TABLE IF NOT EXISTS shifts(

    id SERIAL PRIMARY KEY,

    shift_code VARCHAR(50) UNIQUE,

    shift_name VARCHAR(255),

    start_time TIME,

    end_time TIME,

    standard_workday NUMERIC(10,2),

    late_allow_minutes INTEGER DEFAULT 0,

    early_allow_minutes INTEGER DEFAULT 0
)
"""

with engine.connect() as conn:

    conn.execute(text(sql))

    conn.commit()

print("Shifts table created")