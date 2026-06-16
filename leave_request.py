from database import engine
from sqlalchemy import text
import pandas as pd
from approval import get_department_manager

def create_leave_request(
    employee_code,
    fullname,
    department,
    leave_type,
    start_date,
    end_date,
    total_days,
    reason
):
    main_approver = get_department_manager(
        department
    )

    backup_approver = "admin"
    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO leave_requests(
                employee_code,
                fullname,
                department,
                leave_type,
                start_date,
                end_date,
                total_days,
                reason,
                main_approver,
                backup_approver
            )
            VALUES(
                :employee_code,
                :fullname,
                :department,
                :leave_type,
                :start_date,
                :end_date,
                :total_days,
                :reason,
                :main_approver,
                :backup_approver
            )
            """),
           {
                "employee_code": employee_code,
                "fullname": fullname,
                "department": department,
                "leave_type": leave_type,
                "start_date": start_date,
                "end_date": end_date,
                "total_days": total_days,
                "reason": reason,
                "main_approver": main_approver,
                "backup_approver": backup_approver
            }
        )

        conn.commit()
        
def get_leave_requests():

    with engine.connect() as conn:

        result = conn.execute(
            text("""
            SELECT *
            FROM leave_requests
            ORDER BY created_at DESC
            """)
        )

        rows = result.fetchall()

    return pd.DataFrame(rows)

def approve_leave(
    request_id,
    approver
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE leave_requests
            SET
                status='Đã duyệt',
                approver=:approver,
                approved_at=NOW()
            WHERE id=:id
            """),
            {
                "id": request_id,
                "approver": approver
            }
        )

        conn.commit()
        



def get_pending_requests(
    username,
    role,
    managed_department=None
):

    with engine.connect() as conn:

        if role == "admin":

            result = conn.execute(
                text("""
                SELECT *
                FROM leave_requests
                WHERE status='Chờ duyệt'
                ORDER BY created_at DESC
                """)
            )

        else:

            result = conn.execute(
                text("""
                SELECT *
                FROM leave_requests
                WHERE status='Chờ duyệt'
                AND department=:department
                ORDER BY created_at DESC
                """),
                {
                    "department": managed_department
                }
            )

        rows = result.fetchall()

    return rows


def reject_leave(
    request_id,
    approver,
    note
):

    with engine.connect() as conn:

        conn.execute(
            text("""
            UPDATE leave_requests
            SET
                status='Từ chối',
                approver=:approver,
                approve_note=:note,
                approved_at=NOW()
            WHERE id=:id
            """),
            {
                "id": request_id,
                "approver": approver,
                "note": note
            }
        )

        conn.commit()