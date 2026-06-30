from database import engine
from sqlalchemy import text
import pandas as pd


# =====================================
# THÊM CÔNG VIỆC
# =====================================

def add_task(
    employee_code,
    work_date,
    task_name,
    description="",
    note=""
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO field_checklists(

                    employee_code,
                    work_date,
                    task_name,
                    description,
                    note

                )

                VALUES(

                    :employee_code,
                    :work_date,
                    :task_name,
                    :description,
                    :note

                )
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date,
                "task_name": task_name,
                "description": description,
                "note": note
            }
        )


# =====================================
# LẤY CÔNG VIỆC THEO NGÀY
# =====================================

def get_today_tasks(
    employee_code,
    work_date
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT

                    id,
                    task_name,
                    description,
                    is_completed,
                    note

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date

                ORDER BY id
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )

        rows = result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Công việc",
            "Mô tả",
            "Hoàn thành",
            "Ghi chú"
        ]
    )


# =====================================
# ĐÁNH DẤU HOÀN THÀNH
# =====================================

def complete_task(task_id):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE field_checklists

                SET

                    is_completed=TRUE,

                    completed_time=NOW()

                WHERE id=:id
            """),
            {
                "id": task_id
            }
        )


# =====================================
# CẬP NHẬT GHI CHÚ
# =====================================

def update_note(
    task_id,
    note
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE field_checklists

                SET note=:note

                WHERE id=:id
            """),
            {
                "id": task_id,
                "note": note
            }
        )


# =====================================
# XÓA CÔNG VIỆC
# =====================================

def delete_task(task_id):

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE

                FROM field_checklists

                WHERE id=:id
            """),
            {
                "id": task_id
            }
        )


# =====================================
# ĐẾM CÔNG VIỆC
# =====================================

def get_task_count(
    employee_code,
    work_date
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT COUNT(*)

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )

        return result.scalar()


# =====================================
# ĐẾM ĐÃ HOÀN THÀNH
# =====================================

def get_completed_count(
    employee_code,
    work_date
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT COUNT(*)

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date

                AND

                    is_completed=TRUE
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )

        return result.scalar()
    

# =====================================
# SỬA CÔNG VIỆC
# =====================================

def update_task(
    task_id,
    task_name,
    description,
    note
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE field_checklists

                SET
                    task_name = :task_name,
                    description = :description,
                    note = :note,
                    updated_at = NOW()

                WHERE id = :id
            """),
            {
                "id": task_id,
                "task_name": task_name,
                "description": description,
                "note": note
            }
        )
        
# =====================================
# CHECK IN
# =====================================
def check_in(employee_code, work_date):

    with engine.begin() as conn:

        row = conn.execute(
            text("""
                SELECT id

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date

                LIMIT 1
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        ).fetchone()

        if row:

            conn.execute(
                text("""
                    UPDATE field_checklists
    
                    SET

                        check_in=NOW(),

                        updated_at=NOW()

                    WHERE id=:id
                """),
                {
                    "id": row[0]
                }
            )

        else:

            conn.execute(
                text("""
                    INSERT INTO field_checklists(

                        employee_code,
                        work_date,
                        task_name,
                        description,
                        note,
                        check_in

                    )

                    VALUES(

                        :employee_code,
                        :work_date,
                        '',
                        '',
                        '',
                        NOW()

                    )
                """),
                {
                    "employee_code": employee_code,
                    "work_date": work_date
                }
            )
        
# =====================================
# CHECK OUT
# =====================================

def check_out(
    employee_code,
    work_date
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE field_checklists

                SET
                    check_out = NOW(),
                    updated_at = NOW()

                WHERE
                    employee_code = :employee_code
                AND
                    work_date = :work_date
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )
        

# =====================================
# LẤY THÔNG TIN CHẤM CÔNG
# =====================================

def get_attendance(
    employee_code,
    work_date
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT

                    MIN(check_in),
                    MAX(check_out)

                FROM field_checklists

                WHERE

                    employee_code = :employee_code

                AND

                    work_date = :work_date
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )

        row = result.fetchone()

    return {
        "check_in": row[0],
        "check_out": row[1]
    }
    
# =====================================
# TIẾN ĐỘ
# =====================================

def get_summary(
    employee_code,
    work_date
):

    total = get_task_count(
        employee_code,
        work_date
    )

    completed = get_completed_count(
        employee_code,
        work_date
    )

    percent = 0

    if total > 0:
        percent = completed * 100 / total

    return {
        "total": total,
        "completed": completed,
        "percent": percent
    }
    
# =====================================
# LẤY 1 CÔNG VIỆC
# =====================================

def get_task_by_id(task_id):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *

                FROM field_checklists

                WHERE id=:id
            """),
            {
                "id": task_id
            }
        )

        row = result.fetchone()

    if row is None:
        return None

    return dict(row._mapping)

# =====================================
# RESET CHẤM CÔNG
# =====================================

def reset_checkin_checkout(
    employee_code,
    work_date
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE field_checklists

                SET

                    check_in=NULL,

                    check_out=NULL,

                    updated_at=NOW()

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )
        
# =====================================
# XÓA TOÀN BỘ CÔNG VIỆC
# =====================================

def delete_all_tasks(
    employee_code,
    work_date
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )
        
from sqlalchemy import text
import pandas as pd

# =====================================
# BÁO CÁO NHÂN VIÊN THỊ TRƯỜNG
# =====================================

def get_field_report():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT

                    e.employee_code,
                    e.fullname,
                    e.department,

                    f.work_date,

                    MIN(f.check_in) AS check_in,

                    MAX(f.check_out) AS check_out,

                    COUNT(f.id) AS total_task,

                    SUM(
                        CASE
                            WHEN f.is_completed
                            THEN 1
                            ELSE 0
                        END
                    ) AS completed_task

                FROM employees e

                LEFT JOIN field_checklists f

                    ON e.employee_code=f.employee_code

                WHERE

                    COALESCE(
                        e.employee_type,
                        'office'
                    )='field'

                GROUP BY

                    e.employee_code,
                    e.fullname,
                    e.department,
                    f.work_date

                ORDER BY

                    f.work_date DESC,
                    e.fullname
            """)
        )

        rows=result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Mã NV",
            "Họ tên",
            "Phòng ban",
            "Ngày",
            "Check In",
            "Check Out",
            "Tổng CV",
            "Hoàn thành"
        ]
    )
    
def get_employee_tasks(
    employee_code,
    work_date
):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT

                    task_name,
                    description,
                    note,
                    is_completed,
                    check_in,
                    check_out

                FROM field_checklists

                WHERE

                    employee_code=:employee_code

                AND

                    work_date=:work_date

                ORDER BY id
            """),
            {
                "employee_code": employee_code,
                "work_date": work_date
            }
        )

        rows=result.fetchall()

    return pd.DataFrame(
        rows,
        columns=[
            "Công việc",
            "Mô tả",
            "Ghi chú",
            "Hoàn thành",
            "Check In",
            "Check Out"
        ]
    )