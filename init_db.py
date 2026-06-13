from database import engine
from sqlalchemy import text

with open("schema.sql","r",encoding="utf-8") as f:
    sql = f.read()

with engine.connect() as conn:
    conn.execute(text(sql))
    conn.commit()

print("Database initialized")