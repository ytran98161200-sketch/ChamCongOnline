DEBUG_MODE = True
import streamlit as st
from datetime import datetime
import pytz
VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")
def vn_now():
    return datetime.now(VN_TZ)
import pandas as pd
from streamlit_js_eval import get_geolocation
from utils.gps import check_company_location
from io import BytesIO
from datetime import datetime
from leave_request import (
    create_leave_request,
    get_leave_requests,
    approve_leave,
    reject_leave,
    get_pending_requests,
    get_pending_leave_count,
    is_leave_day, 
    get_leave_notifications,
    mark_notification_read
)
from monthly_report import (
    get_monthly_report,
    export_monthly_report
)
from attendance_log import (
    get_logs_by_date_for_employee,
    get_all_logs,
    get_logs_by_date
)
from auth import (
    login,
    logout
)
from employee import (
    get_user_profile,
    update_user_profile
)

st.set_page_config(
    page_title="Hệ thống chấm công V2",
    layout="centered"
)
st.markdown("""
<style>

/* thu nhỏ menu */
div[data-testid="stPopoverContent"]{
    width: 220px !important;
}

/* nút avatar */
div[data-testid="stPopover"] button{
    border-radius: 20px !important;
    padding: 6px 12px !important;
}

/* nút trong menu */
div[data-testid="stPopoverContent"] button{
    width: 100% !important;
    min-height: 35px !important;
}

</style>
""", unsafe_allow_html=True)
if st.session_state.get(
    "toast_message"
):
    st.toast(
        st.session_state.toast_message
    )

    st.session_state.toast_message = None
st.markdown("""
    
    
<style>
    .stButton > button {
        background: linear-gradient(
            135deg,
            #2196F3,
            #1565C0
        ) !important;

        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #42A5F5,
            #1976D2
        ) !important;

        color: white !important;
    }
@media (max-width:768px){

        .emp-card{
            padding:12px;
        }
        .checkin-wrapper div[data-testid="stButton"] button{
            width:150px;
            height:150px;
            font-size:18px !important;
        }

        h1,h2,h3{
            text-align:center;
        }
        section.main div[data-testid="stButton"] > button{
            width:150px !important;
            height:150px !important;
            font-size:20px !important;
        }
    }
    @keyframes pulse {

    0% {
        box-shadow:
            0 0 0 0 rgba(
                33,
                150,
                243,
                0.6
            );
    }

    70% {
        box-shadow:
            0 0 0 15px rgba(
                33,
                150,
                243,
                0
            );
    }

    100% {
        box-shadow:
            0 0 0 0 rgba(
                33,
                150,
                243,
                0
            );
    }
}
.metric-card {
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    font-weight:bold;
    margin-bottom:15px;
}

.blue {
    background: linear-gradient(
        135deg,
        #2196F3,
        #42A5F5
    );
}

.green {
    background: linear-gradient(
        135deg,
        #4CAF50,
        #66BB6A
    );
}

.orange {
    background: linear-gradient(
        135deg,
        #FF9800,
        #FFB74D
    );
}

.red {
    background: linear-gradient(
        135deg,
        #F44336,
        #EF5350
    );
}

</style>""", unsafe_allow_html=True)
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
# if "checkin_success" not in st.session_state:
#     st.session_state.checkin_success = False
if "create_user_success" not in st.session_state:
    st.session_state.create_user_success = False
if st.session_state.user is None:

    st.title("🕒 HỆ THỐNG CHẤM CÔNG V2")

    with st.form("login_form"):

        username = st.text_input(
            "Tài khoản"
        )

        password = st.text_input(
            "Mật khẩu",
            type="password"
        )

        login_btn = st.form_submit_button(
            "🔑 Đăng nhập",
            use_container_width=True
        )

    if login_btn:

        user = login(
            username,
            password
        )

        if user:
            st.toast(
                "✅ Đăng nhập thành công"
            )

            st.session_state.user = user

            st.rerun()

        else:
            st.error(
                "❌ Sai tài khoản hoặc mật khẩu"
            )

else:

    with st.sidebar:

        st.title("🕒 Chấm Công V2")

        st.success(
            f"👤 {st.session_state.user['username']}"
        )

        role = st.session_state.user["role"]
        pending_leave = get_pending_leave_count()
        st.write("ROLE:", role)
        leave_menu = (
            f"✅ Duyệt đơn ({pending_leave})"
            if pending_leave > 0
            else
            "✅ Duyệt đơn"
        )
        if role == "admin":

            menu = st.selectbox(
                "📋 Chức năng",
                [
                    "📊 Dashboard",
                    "👨‍💼 Nhân viên",
                    "🏢 Phòng ban",
                    "👔 Chức vụ",
                    "🕒 Ca làm việc",
                    "📍 Chấm công",
                    "📋 Nhật ký chấm công",
                    "📝 Đơn từ",
                    leave_menu,
                    "👤 Tài khoản",
                    "📑 Báo cáo",
                    "🔑 Đổi mật khẩu",
                    "📅 Ngày lễ",
                    "📊 Báo cáo tháng"
                ]
            )
        elif role == "approver":

            menu = st.selectbox(
                "📋 Chức năng",
                [
                    "📊 Dashboard",
                    "👨‍💼 Nhân viên",
                    "🕒 Ca làm việc",
                    "📍 Chấm công",
                    "📋 Nhật ký chấm công",
                    "📑 Báo cáo",
                    "🔑 Đổi mật khẩu"
                ]
            )

        elif role == "manager":

            menu = st.selectbox(
                "📋 Chức năng",
                [
                    "📊 Dashboard",
                    "📋 Nhật ký chấm công",
                    leave_menu,
                    "📍 Chấm công",
                    "🔑 Đổi mật khẩu"
                ]
            )

        else:

            menu = st.selectbox(
                "📋 Chức năng",
                [
                    "📍 Chấm công",
                    "📝 Đơn từ",
                    "🔑 Đổi mật khẩu"
                ]
            )
    from datetime import datetime

    header1, header2, header3 = st.columns([8,2,2])

    with header1:
        st.title("🕒 Hệ thống chấm công")

    with header2:
        st.markdown("""
            <div style="
            display:inline-block;
            padding:6px 14px;
            border-radius:20px;
            background:#0f3d1f;
            color:#4ade80;
            font-weight:600;
            font-size:14px;">
            🟢 Online
            </div>
            """, unsafe_allow_html=True)
        st.caption(
            vn_now().strftime("%d/%m/%Y")
        )

    with header3:

        username = "Guest"

        if st.session_state.user:
            username = st.session_state.user["username"]

        with st.popover("👤"):

            st.caption(f"👤 {username}")

            if st.button(
                "📋 Thông tin cá nhân",
                key="profile_btn"
            ):
                st.session_state.page = "profile"
                st.rerun()

            if st.button(
                "🚪 Đăng xuất",
                key="logout_btn"
            ):
                logout()
                                    
            if st.session_state.user is None:
                st.stop()
            user = st.session_state.user

    if (
        user
        and "employee_code" in user
    ):

        notifications = get_leave_notifications(
            user["employee_code"]
        )

        for n in notifications:

            if n["status"] == "Đã duyệt":

                st.success(
                    f"✅ Đơn nghỉ từ {n.start_date} đến {n.end_date} đã được duyệt."
                )

            else:

                st.error(
                    f"❌ Đơn nghỉ từ {n.start_date} đến {n.end_date} đã bị từ chối."
                )

            mark_notification_read(
                n.id
            )
    if st.session_state.page == "profile":
        st.title("👤 Hồ sơ cá nhân")

        col1, col2 = st.columns([3,1])

        with col2:
            if st.button("⬅ Dashboard"):
                st.session_state.page = "dashboard"
                st.rerun()

        profile = get_user_profile(
            st.session_state.user["username"]
        )

        if profile:

            fullname = st.text_input(
                "Họ tên",
                value=profile.get("fullname", "") or ""
            )

            email = st.text_input(
                "Email",
                value=profile.get("email", "") or ""
            )

            phone = st.text_input(
                "Số điện thoại",
                value=profile.get("phone", "") or ""
            )

            if st.button("💾 Lưu thông tin"):

                update_user_profile(
                    st.session_state.user["username"],
                    fullname,
                    email,
                    phone
                )

                st.success("✅ Đã cập nhật")

                st.rerun()

        st.stop()
    if menu == "📊 Dashboard":

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
        st.markdown("""
        <style>

        .dashboard-card{
            border-radius:15px;
            padding:20px;
            color:white;
            text-align:center;
            font-weight:bold;
        }

        .blue{
            background:#2196F3;
        }

        .green{
            background:#4CAF50;
        }

        .orange{
            background:#FF9800;
        }

        .red{
            background:#F44336;
        }
        div[data-testid="stButton"] > button {
            background: #1f77ff;
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            padding: 10px 20px;
        }

        div[data-testid="stButton"] > button:hover {
            background: #005ce6;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
        col1,col2,col3,col4 = st.columns(4)
        with col1:

            st.markdown(f"""
            <div class="dashboard-card blue">
                👥<br>
                Tổng nhân viên
                <h1>{get_employee_count()}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="dashboard-card green">
                ✅<br>
                Đã chấm công
                <h1>{get_today_attendance_count()}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown(f"""
            <div class="dashboard-card orange">
                🕒<br>
                Ca làm việc
                <h1>{get_shift_count()}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col4:

            st.markdown(f"""
            <div class="dashboard-card red">
                ❌<br>
                Chưa chấm công
                <h1>{get_not_attendance_count()}</h1>
            </div>
            """, unsafe_allow_html=True)
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
    elif menu == "👨‍💼 Nhân viên":

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
            employees = get_employees()
            if search:

                employees = employees[
                    employees.astype(str)
                    .apply(
                        lambda x: x.str.contains(
                            search,
                            case=False,
                            na=False
                        )
                    )
                    .any(axis=1)
                ]

            st.dataframe(
                employees,
                use_container_width=True
            )

        with tab2:

            employee_code = st.text_input(
                "Mã nhân viên"
            )

            fullname = st.text_input(
                "Họ tên",
                key="add_employee_name"
            )
            email = st.text_input(
                "Email"
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
                        position,
                        email

                    )

                    st.session_state.toast_message = (
                        f"✅ Đã tạo nhân viên {fullname}"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"❌ Lỗi: {e}")

        with tab3:

            employee_selected = st.selectbox(
                "Chọn nhân viên",
                get_employee_codes()
            )

            employee_data = get_employee(
                employee_selected
            )
            if (
                "selected_employee"
                not in st.session_state
            ):
                st.session_state.selected_employee = ""

            if (
                st.session_state.selected_employee
                != employee_selected
            ):
                st.session_state.selected_employee = employee_selected

                st.session_state.edit_employee_name = (
                    employee_data["fullname"]
                )

                st.session_state.edit_employee_department = (
                    employee_data["department"]
                )

                st.session_state.edit_employee_position = (
                    employee_data["position"]
                )
            fullname_edit = st.text_input(
                "Họ tên",
                key="edit_employee_name"
            )
            department_edit = st.text_input(
                "Phòng ban",
                # value=employee_data["department"],
                key="edit_employee_department"
            )

            position_edit = st.text_input(
                "Chức vụ",
                # value=employee_data["position"],
                key="edit_employee_position"
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

                    st.session_state.toast_message = (
                        "✅ Đã xóa nhân viên"
                    )

                    st.rerun()
    elif menu == "🕒 Ca làm việc":

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

                st.session_state.toast_message = (
                    "✅ Đã lưu ca làm việc"
                )

                st.rerun()

        with col2:

            st.subheader("Danh sách ca")

            st.dataframe(
                get_shifts(),
                use_container_width=True
            )
    elif menu == "📍 Chấm công":
        # if st.session_state.get(
        #     "checkin_success",
        #     False
        # ):
        #     st.success(
        #         f"""
        # ✅ CHẤM CÔNG THÀNH CÔNG

        # 🕒 {vn_now().strftime('%H:%M:%S')}
        # """
        #     )
        from attendance_log import (
            add_log,
            get_today_logs,
            get_today_log_count
        )

        from employee import (
            get_employee_codes
        )

        st.title("📍 Chấm công")
        # left_col = st.container()
        # right_col = st.container()
        st.markdown("""
                    
        <style>
        @keyframes pulse {
            0% {
                box-shadow:0 0 0 0 rgba(33,150,243,.6);
            }
            70% {
                box-shadow:0 0 0 15px rgba(33,150,243,0);
            }
            100% {
                box-shadow:0 0 0 0 rgba(33,150,243,0);
            }
        }
        .emp-card{
            background:linear-gradient(
                135deg,
                #2196F3,
                #42A5F5
            );
            border-radius:20px;
            padding:15px;
            color:white;
            margin-bottom:15px;
        }
        

        .work-card{
            background:linear-gradient(135deg,#FF9800,#FFB74D);
            color:white;
            padding:20px;
            border-radius:20px;
            margin-top:20px;
        }

        /* Nút chấm công */


        /* Hover */
        div[data-testid="stButton"] > button:hover {
            transform:scale(1.05);
            box-shadow:
                0 15px 35px rgba(21,101,192,.5);
        }

        /* Nhấn */
        div[data-testid="stButton"] > button:active {
            transform:scale(.95);
        }
        div[data-testid="stButton"] > button{
            background:#2196F3 !important;
            color:white !important;
            border:none !important;
            border-radius:15px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        with st.container():
            if st.session_state.user["role"] in [
                "employee",
                "manager"
            ]:

                employee_code = st.session_state.user["employee_code"]
                from employee import get_employee

                emp = get_employee(
                    employee_code
                )
                if emp:

                    st.markdown(f"""
                        <div class="emp-card">
                        <h2>👤 {emp['fullname']}</h2>
                        <p>🆔 Mã nhân viên: {employee_code}</p>
                        <p>📅 {vn_now().strftime("%d/%m/%Y")}</p>
                        </div>
                        """, unsafe_allow_html=True)

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
                "📝 Ghi chú (không bắt buộc)",
                height=70
            )
            allow_gps = False
            distance = None
            accuracy = None

            location = get_geolocation(
                component_key="gps_checkin"
            )

            if (
                location
                and "coords" in location
            ):

                lat = location["coords"]["latitude"]
                lon = location["coords"]["longitude"]
                accuracy = location["coords"]["accuracy"]

                if accuracy <= 100:

                    ok, distance = check_company_location(
                        lat,
                        lon
                    )

                    if ok:
                        allow_gps = True

                        st.success(
                            "✅ Bạn đang ở công ty"
                        )

                    else:
                        st.error(
                            "❌ Bạn không ở trong công ty"
                        )

                    st.info(
                        f"""
            📍 Khoảng cách:
            {distance:.0f} m

            🎯 Độ chính xác GPS:
            {accuracy:.0f} m
            """
                    )

                else:

                    st.warning(
                        f"GPS chưa chính xác ({accuracy:.0f}m)"
                    )

            elif (
                location
                and "error" in location
            ):

                st.warning(
                    "⚠️ Vui lòng bật GPS."
                )
            
            import requests
            import platform
            try:
                ip_address = requests.get(
                    "https://api.ipify.org"
                ).text
            except:
                ip_address = "Unknown"
            
            device_info = platform.platform()
            allow_checkin = (
                allow_gps
                or DEBUG_MODE
            )
            if DEBUG_MODE:
                st.warning(
                    "⚠️ Đang ở chế độ TEST - bỏ qua kiểm tra GPS."
                )
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    font-size:30px;
                    font-weight:bold;
                    margin-top:10px;
                    margin-bottom:15px;
                ">
                
                    🕒 {vn_now().strftime("%H:%M:%S")}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            col1, col2, col3 = st.columns([1,2,1])

            with col2:
                st.markdown(
                    '<div class="checkin-btn">',
                    unsafe_allow_html=True
                )


                # with col2:
                check_btn = st.button(
                        "📍 CHẤM CÔNG",
                        key="checkin",
                        use_container_width=True
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )
            if check_btn:

                if not allow_checkin:
                    st.error(
                        "❌ Không thể chấm công ngoài công ty."
                    )
                    st.stop()

                log_count = get_today_log_count(
                    employee_code
                )
                # log_count = get_today_log_count(
                #     employee_code
                # )

                if log_count >= 8:

                    st.error(
                        "❌ Hôm nay đã đủ 8 lần chấm công"
                    )

                    st.stop()
                add_log(
                    employee_code,
                    note,
                    ip_address,
                    device_info,
                    lat,
                    lon,
                    accuracy,
                    distance
                )

                st.session_state.toast_message = (
                    f"📍 Chấm công thành công - "
                    f"{vn_now().strftime('%H:%M:%S')}"
                )

                st.rerun()
            st.divider()

            from datetime import date

            log_count = get_today_log_count(
                employee_code
            )

            st.info(
                f"📍 Hôm nay đã chấm {log_count}/8 lần"
            )
        
        from datetime import datetime

        st.divider()
        
        with st.container():

            st.subheader("📋 Lịch sử chấm công")

            selected_date = st.date_input(
                "📅 Chọn ngày",
                value=date.today(),
                key="history_date"
            )

            logs = get_logs_by_date_for_employee(
                selected_date,
                employee_code
            )

            if logs:

                for i, log in enumerate(logs, start=1):

                    st.success(
                        f"Lần {i} • "
                        f"{log[0].strftime('%H:%M:%S')}"
                    )

            else:

                st.info(
                    "Chưa có dữ liệu chấm công"
                )
                
    elif menu == "👤 Tài khoản":

        from user_management import (
            create_user,
            get_users,
            reset_password,
            get_user,
            update_user
        )
        from employee import get_employees
        st.title("👤 Quản lý tài khoản")

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Danh sách",
                "➕ Tạo tài khoản",
                "✏️ Sửa tài khoản"
            ]
        )

        with tab1:
            users_df = get_users()

            display_df = users_df.copy()
            display_df["role"] = display_df["role"].replace({
                "admin": "Quản trị hệ thống",
                "manager": "Trưởng phòng",
                "approver": "Người duyệt đơn",
                "employee": "Nhân viên"
            })

            display_df.columns = [
                "Tài khoản",
                "Họ tên",
                "Phòng ban",
                "Vai trò",
                "Mã NV",
                "Kích hoạt"
            ]

            edited_df = st.data_editor(
                display_df,
                use_container_width=True,
                hide_index=True,
                disabled=[
                    "Tài khoản",
                    "Họ tên",
                    "Phòng ban",
                    "Mã NV"
                ]
            )
            if st.button("💾 Lưu thay đổi",use_container_width=True):

                role_map = {
                    "Quản trị hệ thống": "admin",
                    "Trưởng phòng": "manager",
                    "Người duyệt đơn": "approver",
                    "Nhân viên": "employee"
                }

                for _, row in edited_df.iterrows():

                    if row["Vai trò"] == "Quản trị hệ thống":
                        is_active = True
                    else:
                        is_active = row["Kích hoạt"]

                    update_user(
                        row["Tài khoản"],
                        role_map[row["Vai trò"]],
                        is_active
                    )

                st.success(
                    "✅ Đã lưu thay đổi"
                )

                st.rerun()
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

                    st.toast(
                        f"✅ Đã tạo tài khoản {username}"
                    )


                    st.rerun()

                except Exception as e:

                    st.error(
                        f"❌ Lỗi tạo tài khoản: {e}"
                    )

                    st.rerun()
        with tab3:

            st.subheader(
                "✏️ Sửa tài khoản"
            )

            users_df = get_users()

            selected_user = st.selectbox(
                "Chọn tài khoản",
                users_df["username"].tolist()
            )

            user_data = get_user(
                selected_user
            )

            role_reverse = {
                "admin": "Quản trị hệ thống",
                "manager": "Trưởng phòng",
                "approver": "Người duyệt đơn",
                "employee": "Nhân viên"
            }

            roles = [
                "Quản trị hệ thống",
                "Trưởng phòng",
                "Người duyệt đơn",
                "Nhân viên"
            ]

            role_display = st.selectbox(
                "Vai trò",
                roles,
                index=roles.index(
                    role_reverse[user_data["role"]]
                )
            )

            is_active = st.checkbox(
                "Kích hoạt",
                value=user_data["is_active"]
            )

            if st.button(
                "💾 Cập nhật tài khoản"
            ):

                role_map = {
                    "Quản trị hệ thống": "admin",
                    "Trưởng phòng": "manager",
                    "Người duyệt đơn": "approver",
                    "Nhân viên": "employee"
                }

                update_user(
                    selected_user,
                    role_map[role_display],
                    is_active
                )

                st.success(
                    "✅ Đã cập nhật tài khoản"
                )

                st.rerun()
    elif menu == "📝 Đơn từ":

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

            if emp is None:

                st.error(
                    "❌ Không tìm thấy thông tin nhân viên"
                )

                st.stop()

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
                )

                st.success(
                    "✅ Đã gửi đơn nghỉ phép"
                )


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
    
    elif menu == "📋 Nhật ký chấm công":

        st.subheader("📋 Nhật ký chấm công")

        selected_date = st.date_input(
            "📅 Chọn ngày"
        )

        log_df = get_logs_by_date(
            selected_date
        )

        if not log_df.empty:
            st.dataframe(
                log_df,
                use_container_width=True
            )
        else:
            st.info(
                "Không có dữ liệu."
            )
    elif menu == "📑 Báo cáo":
        
        from report import attendance_report

        st.subheader("📑 Báo cáo")

        filter_type = st.selectbox(
            "Xem dữ liệu",
            [
            "Hôm nay",
            "Hôm qua",
            "7 ngày gần nhất",
            "30 ngày gần nhất",
            "Tháng này",
            "Tháng trước",
            "Chọn ngày bất kỳ"
                ]
            )

        if filter_type == "Hôm nay":
            df = attendance_report("today")

        elif filter_type == "Hôm qua":
            df = attendance_report("yesterday")

        elif filter_type == "7 ngày gần nhất":
            df = attendance_report("7days")

        elif filter_type == "30 ngày gần nhất":
            df = attendance_report("30days")

        elif filter_type == "Tháng này":
            df = attendance_report("this_month")

        elif filter_type == "Tháng trước":
            df = attendance_report("last_month")

        elif filter_type == "Chọn ngày bất kỳ":

            selected_date = st.date_input(
                "📅 Chọn ngày"
            )

            df = attendance_report(
                "custom",
                selected_date
            )

        else:
            df = attendance_report("today")

        keyword = st.text_input(
            "🔍 Tìm theo mã nhân viên hoặc họ tên"
        )
        if keyword:

            keyword = keyword.lower()

            df = df[
                df["Mã NV"].astype(str)
                .str.lower()
                .str.contains(keyword)
                |
                df["Họ tên"].astype(str)
                .str.lower()
                .str.contains(keyword)
            ]
        st.dataframe(
            df,
            use_container_width=True
        )
        if not df.empty:

            output = BytesIO()

            export_df = df.copy()

            export_df["Ngày"] = (
                export_df["Ngày"]
                .astype(str)
            )

            export_df["Check In"] = (
                export_df["Check In"]
                .astype(str)
            )

            export_df["Check Out"] = (
                export_df["Check Out"]
                .astype(str)
            )

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                export_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Báo cáo"
                )

            st.download_button(
                "📥 Xuất Excel",
                data=output.getvalue(),
                file_name="bao_cao_cham_cong.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:

            st.warning(
                "Không có dữ liệu để xuất Excel."
            )
            
    elif menu == "📅 Ngày lễ":

        from holiday import (
            add_holiday,
            get_holidays
        )

        st.title("📅 Quản lý ngày lễ")

        holiday_date = st.date_input(
            "Ngày lễ"
        )

        holiday_name = st.text_input(
            "Tên ngày lễ"
        )

        if st.button("💾 Lưu ngày lễ"):

            add_holiday(
                holiday_date,
                holiday_name
            )

            st.toast(
                "Đã lưu ngày lễ"
            )

            st.rerun()

        st.divider()

        st.dataframe(
            get_holidays(),
            use_container_width=True
        )
    elif menu == "🏢 Phòng ban":

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

            st.session_state.toast_message = (
                "✅ Đã thêm phòng ban"
            )

            st.rerun()

    elif menu == "👔 Chức vụ":

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

            st.toast(
                "Đã thêm chức vụ"
            )

            st.rerun()
            
    

    elif menu.startswith("✅ Duyệt đơn"):

        from leave_request import (
            get_pending_requests,
            approve_leave,
            reject_leave,
            get_pending_leave_count,
            is_leave_day
        )

        user = st.session_state.user
        requests = get_pending_requests(
            user["username"],
            user["role"],
            user.get("managed_department")
        )
        pending_leave = get_pending_leave_count()
        st.title("📋 Duyệt đơn")
        st.info(
            f"Có {pending_leave} đơn chờ duyệt"
        )

        if not requests:
            st.success("Không có đơn cần duyệt")
        else:

            for r in requests:

                st.markdown(
                    f"""
                    👤 {r.fullname}

                    🏢 {r.department}

                    📅 {r.start_date}
                    → {r.end_date}

                    📝 {r.reason}
                    """
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        f"✅ Duyệt {r.id}"
                    ):
                        approve_leave(
                            r.id,
                            user["username"]
                        )
                        st.success("Đã duyệt")
                        st.rerun()

                with col2:
                    if st.button(
                        f"❌ Từ chối {r.id}"
                    ):
                        reject_leave(
                            r.id,
                            user["username"],
                            "Từ chối"
                        )
                        st.success("Đã từ chối")
                        st.rerun()

                st.divider()
    elif menu == "🔑 Đổi mật khẩu":

        from user_management import change_password

        st.subheader("🔑 Đổi mật khẩu")

        old_password = st.text_input(
            "Mật khẩu hiện tại",
            type="password"
        )

        new_password = st.text_input(
            "Mật khẩu mới",
            type="password"
        )

        confirm_password = st.text_input(
            "Nhập lại mật khẩu mới",
            type="password"
        )

        if st.button(
            "💾 Đổi mật khẩu",
            use_container_width=True
        ):

            if not old_password:
                st.error(
                    "❌ Vui lòng nhập mật khẩu hiện tại"
                )

            elif not new_password:
                st.error(
                    "❌ Vui lòng nhập mật khẩu mới"
                )

            elif new_password != confirm_password:
                st.error(
                    "❌ Mật khẩu xác nhận không khớp"
                )

            elif len(new_password) < 6:
                st.error(
                    "❌ Mật khẩu phải từ 6 ký tự trở lên"
                )

            else:

                success = change_password(
                    st.session_state.user["username"],
                    old_password,
                    new_password
                )

                if success:

                    st.toast(
                        "✅ Đổi mật khẩu thành công"
                    )

                    st.info(
                        "Vui lòng đăng nhập lại"
                    )

                else:

                    st.error(
                        "❌ Mật khẩu hiện tại không đúng"
                    )
    elif menu == "📊 Báo cáo tháng":
        st.subheader(
            "📊 Báo cáo chấm công tháng"
        )

        col1, col2 = st.columns(2)

        with col1:
            month = st.selectbox(
                "Tháng",
                range(1, 13)
            )

        with col2:
            year = st.selectbox(
                "Năm",
                range(2025, 2031)
            )

        df = get_monthly_report(
            month,
            year
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📊 Xem báo cáo"
            ):
                st.rerun()

        with col2:

            output = export_monthly_report(
                month,
                year
            )

            st.download_button(
                "📥 Xuất Excel",
                data=output.getvalue(),
                file_name=f"BCCVP_{month}_{year}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )