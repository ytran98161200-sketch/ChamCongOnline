from database import engine
from sqlalchemy import text
import bcrypt

def login(username,password):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
            SELECT
                u.*,
                e.employee_type,
                e.fullname,
                e.department,
                e.company_id
            FROM users u
            LEFT JOIN employees e
            ON u.employee_code = e.employee_code
            WHERE u.username=:username
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
        user_data = dict(user._mapping)

        if "employee_type" not in user_data:
            user_data["employee_type"] = "office"

        return user_data

    return None

import streamlit as st

def logout():
    st.session_state.user = None
    st.session_state.page = "dashboard"
    st.rerun()