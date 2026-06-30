from sqlalchemy import text
from database import engine


# ======================================================
# LẤY DANH SÁCH CÔNG TY
# ======================================================
def get_companies(active_only=False):
    """
    Lấy danh sách công ty

    active_only=True -> chỉ lấy công ty đang hoạt động
    """

    sql = """
        SELECT
            id,
            company_code,
            company_name,
            short_name,
            tax_code,
            website,
            address,
            phone,
            email,
            logo,
            theme_color,
            status,
            created_at
        FROM companies
    """

    if active_only:
        sql += " WHERE status='Hoạt động'"

    sql += " ORDER BY company_name"

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return result.mappings().all()


# ======================================================
# LẤY 1 CÔNG TY
# ======================================================
def get_company(company_id):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM companies
                WHERE id=:id
            """),
            {
                "id": company_id
            }
        )

        return result.mappings().first()


# ======================================================
# LẤY ID CÔNG TY THEO TÊN
# ======================================================
def get_company_by_name(company_name):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT id
                FROM companies
                WHERE company_name=:company_name
            """),
            {
                "company_name": company_name
            }
        )

        row = result.fetchone()

    return row[0] if row else None


# ======================================================
# LẤY THEO MÃ CÔNG TY
# ======================================================
def get_company_by_code(company_code):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM companies
                WHERE company_code=:company_code
            """),
            {
                "company_code": company_code
            }
        )

        return result.mappings().first()


# ======================================================
# KIỂM TRA TRÙNG MÃ
# ======================================================
def company_exists(company_code):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM companies
                WHERE company_code=:company_code
            """),
            {
                "company_code": company_code
            }
        )

        return result.scalar() > 0


# ======================================================
# THÊM CÔNG TY
# ======================================================
def add_company(
    company_code,
    company_name,
    short_name,
    tax_code,
    website,
    address,
    phone,
    email,
    logo="",
    theme_color="#0E7490",
    status="Hoạt động"
):

    if company_exists(company_code):
        return False

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO companies(

                    company_code,
                    company_name,
                    short_name,
                    tax_code,
                    website,
                    address,
                    phone,
                    email,
                    logo,
                    theme_color,
                    status

                )

                VALUES(

                    :company_code,
                    :company_name,
                    :short_name,
                    :tax_code,
                    :website,
                    :address,
                    :phone,
                    :email,
                    :logo,
                    :theme_color,
                    :status

                )
            """),
            {
                "company_code": company_code,
                "company_name": company_name,
                "short_name": short_name,
                "tax_code": tax_code,
                "website": website,
                "address": address,
                "phone": phone,
                "email": email,
                "logo": logo,
                "theme_color": theme_color,
                "status": status
            }
        )

    return True


# ======================================================
# CẬP NHẬT
# ======================================================
def update_company(
    company_id,
    company_code,
    company_name,
    short_name,
    tax_code,
    website,
    address,
    phone,
    email,
    logo,
    theme_color,
    status
):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE companies
                SET
                    company_code=:company_code,
                    company_name=:company_name,
                    short_name=:short_name,
                    tax_code=:tax_code,
                    website=:website,
                    address=:address,
                    phone=:phone,
                    email=:email,
                    logo=:logo,
                    theme_color=:theme_color,
                    status=:status
                WHERE id=:id
            """),
            {
                "id": company_id,
                "company_code": company_code,
                "company_name": company_name,
                "short_name": short_name,
                "tax_code": tax_code,
                "website": website,
                "address": address,
                "phone": phone,
                "email": email,
                "logo": logo,
                "theme_color": theme_color,
                "status": status
            }
        )

    return True


# ======================================================
# KIỂM TRA CÓ ĐƯỢC XÓA KHÔNG
# ======================================================
def can_delete_company(company_id):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM employees
                WHERE company_id=:company_id
            """),
            {
                "company_id": company_id
            }
        )

        return result.scalar() == 0


# ======================================================
# XÓA
# ======================================================
def delete_company(company_id):

    if not can_delete_company(company_id):
        return False

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE
                FROM companies
                WHERE id=:id
            """),
            {
                "id": company_id
            }
        )

    return True


# ======================================================
# ĐẾM NHÂN VIÊN
# ======================================================
def get_company_employee_count(company_id):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT COUNT(*)
                FROM employees
                WHERE company_id=:company_id
            """),
            {
                "company_id": company_id
            }
        )

        return result.scalar()


# ======================================================
# TÌM KIẾM
# ======================================================
def search_companies(keyword):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM companies
                WHERE
                    company_name ILIKE :kw
                    OR company_code ILIKE :kw
                ORDER BY company_name
            """),
            {
                "kw": f"%{keyword}%"
            }
        )

        return result.mappings().all()


# ======================================================
# ĐỔI TRẠNG THÁI
# ======================================================
def toggle_company_status(company_id):

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE companies
                SET status=
                    CASE
                        WHEN status='Hoạt động'
                        THEN 'Ngừng hoạt động'
                        ELSE 'Hoạt động'
                    END
                WHERE id=:id
            """),
            {
                "id": company_id
            }
        )
        
# =====================================
# DANH SÁCH TÊN CÔNG TY
# =====================================

def get_company_names():

    companies = get_companies(active_only=True)

    return [
        company["company_name"]
        for company in companies
    ]