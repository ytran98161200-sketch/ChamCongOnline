from database import engine
from sqlalchemy import text
import bcrypt

def login(username,password):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
            SELECT *
            FROM users
            WHERE username=:username
            """),
            {"username":username}
        ).fetchone()

    if not user:
        return None
    if user.is_active is False:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user.password_hash.encode()
    ):
        return dict(user._mapping)

    return None