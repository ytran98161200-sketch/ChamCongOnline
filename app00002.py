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
            st.toast("✅ Đăng nhập thành công")
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
                "Phòng ban",
                "Chức vụ",
                "Ca làm việc",
                "Chấm công",
                "Nhật ký chấm công",
                "Đơn từ",
                "Duyệt đơn",
                "Tài khoản",
                "Báo cáo"
            ]
        )

    elif role == "approver":

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
                "Chấm công",
                "Đơn từ"
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

            st.toast(
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

            from department import get_departments

            department = st.selectbox(
                "Phòng ban",
                get_departments()
            )

            from position import get_positions

            position = st.selectbox(
                "Chức vụ",
                get_positions()
            )

        if st.button("💾 Lưu nhân viên"):

            try:

                add_employee(
                    employee_code,
                    fullname,
                    department,
                    position
                )

                st.success(
                    f"✅ Đã tạo nhân viên {fullname}"
                )

                st.rerun()

            except Exception:

                st.error(
                    f"❌ Mã nhân viên {employee_code} đã tồn tại"
                )

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

                    st.toast(
                        "✅ Đã cập nhật"
                    )

                    st.rerun()

            with col2:

                if st.button("🗑️ Xóa nhân viên"):

                    delete_employee(
                        employee_selected
                    )

                    st.toast(
                        "✅ Đã xóa"
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

                st.toast("✅ Đã lưu ca")

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
            from employee import get_employee

            emp = get_employee(
                employee_code
            )
            if emp:

                st.info(
                    f"👤 Nhân viên: {employee_code} - {emp['fullname']}"
                )

            else:

                st.warning(
                    f"👤 Nhân viên: {employee_code}"
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

            st.toast("✅ Đã ghi nhận chấm công")

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
    elif menu == "Tài khoản":

        from user_management import (
            create_user,
            get_users,
            reset_password
        )
        from employee import get_employees
        st.title("👤 Quản lý tài khoản")

        tab1, tab2 = st.tabs(
            [
                "📋 Danh sách",
                "➕ Tạo tài khoản"
            ]
        )

        with tab1:

            users_df = get_users()

            st.dataframe(
                users_df,
                use_container_width=True
            )

            usernames = users_df["username"].tolist()

            selected_user = st.selectbox(
                "Chọn tài khoản cần reset mật khẩu",
                usernames
            )

            new_password = st.text_input(
                "Mật khẩu mới",
                type="password"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button("🔑 Đổi mật khẩu"):

                    reset_password(
                        selected_user,
                        new_password
                    )

                    st.success(
                        f"Đã đặt lại mật khẩu cho {selected_user}"
                    )

            with col2:

                if st.button("🔄 Reset về 123456"):

                    reset_password(
                        selected_user,
                        "123456"
                    )

                    st.success(
                        f"Đã đặt lại mật khẩu cho {selected_user}"
                    )

                    # reset_password(
                    #     selected_user,
                    #     new_password
                    # )

                    # st.success(
                    #     f"Đã đặt lại mật khẩu cho {selected_user}"
                    # )

        with tab2:

            username = st.text_input(
                "Tên đăng nhập"
            )

            password = st.text_input(
                "Mật khẩu",
                type="password"
            )

            role_display = st.selectbox(
                "Vai trò",
                [
                    "Admin",
                    "Trưởng phòng",
                    "Người duyệt đơn",
                    "Nhân viên"
                ]
            )
            managed_department = None
            if role_display == "Trưởng phòng":

                from department import get_departments

                managed_department = st.selectbox(
                    "Phòng ban phụ trách",
                    get_departments()
                )
            role_map = {
                "Admin": "admin",
                "Trưởng phòng": "manager",
                "Người duyệt đơn": "approver",
                "Nhân viên": "employee"
            }
            # employee_code = st.text_input(
            #     "Mã nhân viên"
            # )
            employees = get_employees()

            employee_options = {}

            for _, row in employees.iterrows():

                display = f"{row['Mã NV']} - {row['Họ tên']}"

                employee_options[display] = row['Mã NV']

            if employee_options:

                employee_selected = st.selectbox(
                    "Nhân viên",
                    list(employee_options.keys())
                )

                employee_code = employee_options[
                    employee_selected
                ]

            else:

                st.warning(
                    "Chưa có nhân viên nào"
                )

                employee_code = ""
            if st.button("Tạo tài khoản"):

                try:

                    create_user(
                        username,
                        password,
                        role_map[role_display],
                        employee_code,
                        managed_department
                    )

                    st.success(
                        f"✅ Đã tạo tài khoản {username}"
                    )

                    st.balloons()

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Lỗi tạo tài khoản: {e}"
                    )

                    st.rerun()
    elif menu == "Đơn từ":

        tab1, tab2 = st.tabs(
            [
                "📄 Nghỉ phép",
                "🕒 Cập nhật công"
            ]
        )

        with tab1:

            st.subheader(
                "📄 Đăng ký nghỉ phép"
            )

            leave_type = st.selectbox(
                "Loại nghỉ",
                [
                    "Nghỉ phép",
                    # "Nghỉ bệnh",
                    "Nghỉ không lương"
                ]
            )

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input(
                    "Từ ngày"
                )

                start_time = st.time_input(
                    "Từ giờ"
                )

            with col2:

                end_date = st.date_input(
                    "Đến ngày"
                )

                end_time = st.time_input(
                    "Đến giờ"
                )
            st.info(
                f"Từ {start_date} {start_time} đến {end_date} {end_time}"
            )
            leave_session = st.selectbox(
                "Hình thức nghỉ",
                [
                    "Cả ngày",
                    "Nửa ngày sáng",
                    "Nửa ngày chiều"
                ]
            )
            reason = st.text_area(
                "Lý do nghỉ"
            )
            from employee import get_employee
            from approval import get_department_manager

            emp = get_employee(
                st.session_state.user["employee_code"]
            )

            department = emp["department"]

            fullname = emp["fullname"]

            manager = get_department_manager(
                department
            )

            if manager:

                st.info(
                    f"👨‍💼 Người duyệt chính: {manager['fullname']}"
                )

            else:

                st.warning(
                    "Chưa cấu hình trưởng phòng"
                )

            st.info(
                "👑 Người duyệt phụ: admin"
            )
            total_days = (
                end_date - start_date
            ).days + 1

            st.info(
                f"Số ngày nghỉ: {total_days}"
            )

            if st.button(
                "📨 Gửi đơn nghỉ phép"
            ):

                create_leave_request(
                    st.session_state.user["employee_code"],
                    fullname,
                    department,
                    leave_type,
                    start_date,
                    end_date,
                    total_days,
                    reason, 
                    manager["employee_code"]
                )

                st.success(
                    "✅ Đã gửi đơn nghỉ phép"
                )

                st.balloons()

                st.rerun()

        with tab2:

            st.subheader(
                "🕒 Xin cập nhật công"
            )

            request_date = st.date_input(
                "Ngày cần cập nhật"
            )

            check_in = st.time_input(
                "Giờ vào"
            )

            check_out = st.time_input(
                "Giờ ra"
            )

            reason2 = st.text_area(
                "Lý do cập nhật công"
            )

            if st.button(
                "📨 Gửi yêu cầu cập nhật công"
            ):

                st.success(
                    "Đã gửi yêu cầu cập nhật công"
                )
    elif menu == "Báo cáo":
        st.title("📑 Báo cáo")

        from report import attendance_report

        report_df = attendance_report()

        st.dataframe(
            report_df,
            use_container_width=True
        )
        excel_data = report_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 Xuất Excel",
            excel_data,
            file_name="bao_cao_cham_cong.csv",
            mime="text/csv"
        )
    elif menu == "Phòng ban":

        from department import (
            get_departments,
            add_department
        )

        st.title("🏢 Quản lý phòng ban")

        st.write(
            get_departments()
        )

        new_department = st.text_input(
            "Tên phòng ban mới"
        )

        if st.button(
            "➕ Thêm phòng ban"
        ):

            add_department(
                new_department
            )

            st.success(
                "Đã thêm phòng ban"
            )

            st.rerun()

    elif menu == "Chức vụ":

        from position import (
            get_positions,
            add_position
        )

        st.title("👔 Quản lý chức vụ")

        positions = get_positions()

        for p in positions:

            st.write(
                "•",
                p
            )

        new_position = st.text_input(
            "Tên chức vụ mới"
        )

        if st.button(
            "➕ Thêm chức vụ"
        ):

            add_position(
                new_position
            )

            st.success(
                "Đã thêm chức vụ"
            )

            st.rerun()
            
    
    elif menu == "Đơn từ":
        from leave_request import (
            create_leave_request
        )

        tab1, tab2 = st.tabs(
            [
                "📄 Nghỉ phép",
                "🕒 Cập nhật công"
            ]
        )
    elif menu == "Duyệt đơn":

        from leave_request import (
            get_pending_requests,
            approve_leave,
            reject_leave
        )

        user = st.session_state.user

        requests = get_pending_requests(
            user["username"],
            user["role"],
            user.get("managed_department")
        )

        st.title("📋 Duyệt đơn")