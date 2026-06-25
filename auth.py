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
        from datetime import datetime

        with engine.begin() as conn:

            conn.execute(
                text("""
                UPDATE users
                SET last_login=:last_login
                WHERE username=:username
                """),
                {
                    "last_login": datetime.now(),
                    "username": username
                }
            )
        return dict(user._mapping)

    return None

import streamlit as st

def logout():
    st.session_state.user = None
    st.session_state.page = "dashboard"
    st.rerun()