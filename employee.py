from database import engine
from sqlalchemy import text
import pandas as pd

def add_employee(
    company_id,
    department_id,
    employee_code,
    fullname,
    department,
    position,
    email,
    employee_type="office"
):
    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO employees(
                employee_code,
                fullname,
                company_id,
                department_id,
                department,
                position,
                email,
                employee_type,
                status
            )
            VALUES(
                :employee_code,
                :fullname,
                :company_id,
                :department_id,
                :department,
                :position,
                :email,
                :employee_type,
                'Đang làm'
            )
            """),
            
                {
                "employee_code": employee_code,
                "fullname": fullname,
                "company_id": company_id,
                "department_id": department_id,
                "department": department,
                "position": position,
                "email": email,
                "employee_type": employee_type
            }
        )

        conn.commit()


def get_employees(keyword=""):

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    e.employee_code,
                    e.fullname,
                    COALESCE(e.employee_type,'office'),
                    e.department,
                    e.position,
                    COALESCE(s.shift_name,'Chưa gán'),
                    COALESCE(e.status,'Đang làm')

            FROM employees e

            LEFT JOIN shifts s
                ON e.shift_code=s.shift_code

            WHERE
                e.employee_code ILIKE :keyword
                OR e.fullname ILIKE :keyword

            ORDER BY e.fullname
            """),
            {
                "keyword": f"%{keyword}%"
            }
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Họ tên",
            "Loại NV",
            "Phòng ban",
            "Chức vụ",
            "Ca làm",
            "Trạng thái"
        ]
    )
def delete_employee(employee_code):

    with engine.connect() as conn:

        conn.execute(
            text("""
            DELETE FROM employees
            WHERE employee_code=:employee_code
            """),
            {
                "employee_code": employee_code
            }
        )

        conn.commit()
def get_employee_codes():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT employee_code
            FROM employees
            ORDER BY employee_code
            """)
        )

        rows = result.fetchall()

    return [r[0] for r in rows]

def assign_shift(
    employee_code,
    shift_code
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE employees
            SET shift_code=:shift_code
            WHERE employee_code=:employee_code
            """),
            {
                "shift_code": shift_code,
                "employee_code": employee_code
            }
        )

        conn.commit()
        
        
def update_employee(
    employee_code,
    fullname,
    department,
    position,
    shift_code,
    employee_type
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE employees
            SET
                fullname=:fullname,
                department=:department,
                position=:position,
                shift_code=:shift_code,
                employee_type=:employee_type
            WHERE employee_code=:employee_code
            """),
            {
                "employee_code": employee_code,
                "fullname": fullname,
                "department": department,
                "position": position,
                "shift_code": shift_code,
                "employee_type": employee_type
            }
        )

        conn.commit()


def get_employee(employee_code):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                employee_code,
                fullname,
                company_id,
                department_id,
                department,
                position,
                email,
                employee_type,
                shift_code
            FROM employees
            WHERE employee_code=:employee_code
            """),
            {
                "employee_code": employee_code
            }
        )

        row = result.fetchone()

    if not row:
        return None

    return {
        "employee_code": row[0],
        "fullname": row[1],
        "company_id": row[2],
        "department_id": row[3],
        "department": row[4],
        "position": row[5],
        "email": row[6],
        "employee_type": row[7],
        "shift_code": row[8]
    }

def get_employee_count():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM employees
            """)
        )

        return result.scalar()


def get_active_employee_count():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT COUNT(*)
            FROM employees
            WHERE COALESCE(status,'Đang làm')='Đang làm'
            """)
        )

        return result.scalar()
    
def get_not_attendance_count():

    from attendance_log import (
        get_today_attendance_count
    )

    total = get_employee_count()

    checked = get_today_attendance_count()

    return total - checked

def get_not_attendance_employees():

    from attendance_log import (
        get_today_attendance_employees
    )

    checked = get_today_attendance_employees()

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT
                employee_code,
                fullname
            FROM employees
            ORDER BY fullname
            """)
        )

        rows = result.fetchall()

    return [
        row
        for row in rows
        if row[0] not in checked
    ]
    
from database import engine
from sqlalchemy import text

def get_user_profile(username):

    with engine.connect() as conn:

        user = conn.execute(
            text("""
            SELECT *
            FROM users
            WHERE username=:username
            """),
            {
                "username": username
            }
        ).mappings().first()

    return user

def update_user_profile(
    username,
    fullname,
    email,
    phone
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE users
                SET
                    fullname = :fullname,
                    email = :email,
                    phone = :phone
                WHERE username = :username
            """),
            {
                "fullname": fullname,
                "email": email,
                "phone": phone,
                "username": username
            }
        )