import streamlit as st
from auth import login

st.set_page_config(
    page_title="Hệ thống chấm công V2",
    layout="wide"
)

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:

    st.title("🕒 HỆ THỐNG CHẤM CÔNG V2")

    username = st.text_input(
        "Tài khoản"
    )

    password = st.text_input(
        "Mật khẩu",
        type="password"
    )

    if st.button("Đăng nhập"):

        user = login(
            username,
            password
        )

        if user:

            st.session_state.user = user

            st.rerun()

        else:

            st.error(
                "Sai tài khoản hoặc mật khẩu"
            )

else:

    with st.sidebar:

        st.title("🕒 Chấm Công V2")

        st.success(
            f"👤 {st.session_state.user['username']}"
        )

        role = st.session_state.user["role"]

    if role == "admin":

        menu = st.radio(
            "Chọn chức năng",
            [
                "Dashboard",
                "Nhân viên",
                "Ca làm việc",
                "Chấm công",
                "Nhật ký chấm công",
                "Tài khoản",
                "Báo cáo"
            ]
        )

    elif role == "hr":

        menu = st.radio(
            "Chọn chức năng",
            [
                "Dashboard",
                "Nhân viên",
                "Ca làm việc",
                "Chấm công",
                "Nhật ký chấm công",
                "Báo cáo"
            ]
        )

    elif role == "manager":

        menu = st.radio(
            "Chọn chức năng",
            [
                "Dashboard",
                "Nhật ký chấm công",
                "Duyệt phép"
            ]
        )

    else:

        menu = st.radio(
            "Chọn chức năng",
            [
                "Chấm công"
            ]
        )

    if st.button("🚪 Đăng xuất",use_container_width=True):

            st.session_state.user = None

            st.rerun()

    if menu == "Dashboard":

        from employee import (
            get_employee_count,
            get_active_employee_count,
            get_not_attendance_count,
            get_not_attendance_employees
        )
        
        from attendance_log import (
            get_today_attendance_count,
            get_today_note_count
        )
        from shift import (
            get_shift_count
        )

        st.title("📊 Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "👨‍💼 Tổng nhân viên",
                get_employee_count()
            )

        with col2:

            st.metric(
                "🕒 Tổng ca làm việc",
                get_shift_count()
            )

        # with col3:

        #     st.metric(
        #         "✅ Đang làm",
        #         get_active_employee_count()
        #     )
        with col3:

            st.metric(
                "📍 Đã chấm công",
                get_today_attendance_count()
            )
        with col4:

            st.metric(
                "❌ Chưa chấm công",
                get_not_attendance_count()
            )
        st.divider()

        st.metric(
            "📝 Có ghi chú hôm nay",
            get_today_note_count()
        )
        st.divider()

        st.subheader(
            "❌ Nhân viên chưa chấm công hôm nay"
        )

        missing = get_not_attendance_employees()

        if missing:

            for emp in missing:

                st.warning(
                    f"{emp[0]} - {emp[1]}"
                )

        else:

            st.success(
                "Tất cả nhân viên đã chấm công"
            )
    elif menu == "Nhân viên":

        from employee import (
            add_employee,
            get_employees,
            get_employee_codes,
            get_employee,
            update_employee,
            delete_employee
        )

        from shift import get_shift_codes

        st.title("👨‍💼 Quản lý nhân viên")

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Danh sách",
                "➕ Thêm nhân viên",
                "✏️ Sửa / 🗑️ Xóa"
            ]
        )

        with tab1:

            search = st.text_input(
                "🔍 Tìm kiếm nhân viên"
            )

            st.dataframe(
                get_employees(search),
                use_container_width=True
            )

        with tab2:

            employee_code = st.text_input(
                "Mã nhân viên"
            )

            fullname = st.text_input(
                "Họ tên"
            )

            department = st.text_input(
                "Phòng ban"
            )

            position = st.text_input(
                "Chức vụ"
            )

        if st.button("💾 Lưu nhân viên"):

            add_employee(
                employee_code,
                fullname,
                department,
                position
            )

            st.success(
                "Đã lưu nhân viên"
            )

            st.rerun()

        with tab3:

            employee_selected = st.selectbox(
                "Chọn nhân viên",
                get_employee_codes()
            )

            employee_data = get_employee(
                employee_selected
            )

            fullname_edit = st.text_input(
                "Họ tên",
                value=employee_data["fullname"]
            )

            department_edit = st.text_input(
                "Phòng ban",
                value=employee_data["department"]
            )

            position_edit = st.text_input(
                "Chức vụ",
                value=employee_data["position"]
            )

            shift_edit = st.selectbox(
                "Ca làm",
                get_shift_codes()
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("✏️ Cập nhật"):

                    update_employee(
                        employee_selected,
                        fullname_edit,
                        department_edit,
                        position_edit,
                        shift_edit
                    )

                    st.success(
                        "Đã cập nhật"
                    )

                    st.rerun()

            with col2:

                if st.button("🗑️ Xóa nhân viên"):

                    delete_employee(
                        employee_selected
                    )

                    st.success(
                        "Đã xóa"
                    )

                    st.rerun()
    elif menu == "Ca làm việc":

        from shift import (
            add_shift,
            get_shifts
        )

        st.title("🕒 Quản lý ca làm việc")

        col1, col2 = st.columns(2)

        with col1:

            shift_code = st.text_input("Mã ca")

            shift_name = st.text_input("Tên ca")

            start_time = st.time_input("Giờ vào")

            end_time = st.time_input("Giờ ra")

            standard_workday = st.number_input(
                "Công chuẩn",
                value=1.0
            )

            late_allow = st.number_input(
                "Cho phép trễ (phút)",
                value=15
            )

            early_allow = st.number_input(
                "Cho phép về sớm (phút)",
                value=15
            )

            if st.button("Lưu ca làm việc"):

                add_shift(
                    shift_code,
                    shift_name,
                    start_time,
                    end_time,
                    standard_workday,
                    late_allow,
                    early_allow
                )

                st.success("Đã lưu ca")

                st.rerun()

        with col2:

            st.subheader("Danh sách ca")

            st.dataframe(
                get_shifts(),
                use_container_width=True
            )
    elif menu == "Chấm công":
        from attendance_log import (
            add_log,
            get_today_logs
        )

        from employee import (
            get_employee_codes
        )

        st.title("📍 Chấm công")

        if st.session_state.user["role"] == "employee":

            employee_code = st.session_state.user["employee_code"]

            st.info(
                f"Nhân viên: {employee_code}"
            )

        else:

            employee_code = st.selectbox(
                "Nhân viên",
                get_employee_codes()
            )
        note = st.text_area(
            "📝 Ghi chú (không bắt buộc)"
        )
        if st.button(
            "📍 CHẤM CÔNG",
            use_container_width=True
        ):

            add_log(
                employee_code,
                note
            )

            st.success(
                "Đã ghi nhận chấm công"
            )

            st.rerun()
        st.divider()

        logs = get_today_logs(employee_code)

        st.subheader(
            "Lịch sử hôm nay"
        )

        for i, log in enumerate(logs, start=1):
            st.write(f"Lần {i}: {log[0]}")
            
    elif menu == "Nhật ký chấm công":

        from attendance_log import (
            get_logs_by_date,
            get_daily_summary
        )

        from employee import (
            get_employee_codes
        )

        st.title(
            "📊 Nhật ký chấm công"
        )

        selected_date = st.date_input(
            "📅 Chọn ngày"
        )
        employee_filter = st.selectbox(
            "👤 Nhân viên",
            ["Tất cả"] + get_employee_codes()
        )
        logs = get_logs_by_date(
            selected_date,
            employee_filter
        )

        st.dataframe(
            logs,
            use_container_width=True
        )
        
        st.divider()

        st.subheader(
            "📋 Tổng hợp công trong ngày"
        )

        summary = get_daily_summary(
            selected_date
        )

        st.dataframe(
            summary,
            use_container_width=True
        )
    elif menu == "Báo cáo":
        st.title(
            "📑 Báo cáo"
        )