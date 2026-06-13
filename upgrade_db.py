from database import engine
from sqlalchemy import text

sqls = [

"""
ALTER TABLE employees
ADD COLUMN IF NOT EXISTS email VARCHAR(255)
""",

"""
ALTER TABLE employees
ADD COLUMN IF NOT EXISTS phone VARCHAR(50)
""",

"""
ALTER TABLE employees
ADD COLUMN IF NOT EXISTS shift_name VARCHAR(100)
""",

"""
ALTER TABLE employees
ADD COLUMN IF NOT EXISTS status VARCHAR(50)
DEFAULT 'Đang làm'
""",

"""
ALTER TABLE employees
ADD COLUMN IF NOT EXISTS hire_date DATE
"""

]

with engine.connect() as conn:

    for sql in sqls:
        conn.execute(text(sql))

    conn.commit()

print("Upgrade completed")