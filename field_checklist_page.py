import streamlit as st
import pandas as pd
from datetime import date

from field_checklist import (
    add_task,
    get_today_tasks,
    complete_task,
    delete_task,
    update_note,
    update_task,
    get_task_by_id,
    check_in,
    check_out,
    get_attendance,
    get_summary
)


def show_field_checklist():

    st.title("📝 Công việc nhân viên thị trường")

    user = st.session_state.user

    employee_code = user["employee_code"]

    work_date = st.date_input(
        "📅 Ngày làm việc",
        value=date.today(),
        format="DD/MM/YYYY"
    )

    st.divider()

    show_attendance(
        employee_code,
        work_date
    )

    st.divider()

    show_summary(
        employee_code,
        work_date
    )

    st.divider()

    add_task_form(
        employee_code,
        work_date
    )

    st.divider()

    show_task_table(
        employee_code,
        work_date
    )
    
def show_attendance(
    employee_code,
    work_date
):

    st.subheader("🕒 Chấm công")

    attendance = get_attendance(
        employee_code,
        work_date
    )
    if attendance["check_in"]:

        st.success(
            f"✅ Đã Check In: {attendance['check_in']}"
        )

    else:

        st.warning(
            "⚠️ Chưa Check In"
        )


    if attendance["check_out"]:

        st.success(
            f"✅ Đã Check Out: {attendance['check_out']}"
        )

    else:

        st.warning(
            "⚠️ Chưa Check Out"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.write("Check In")

        st.write(attendance["check_in"])

        if st.button(
            "📍 Check In",
            key="field_checkin"
        ):

            check_in(
                employee_code,
                work_date
            )

            st.success(
                "Check In thành công"
            )

            st.rerun()

    with col2:

        st.write("Check Out")

        st.write(attendance["check_out"])

        if st.button(
            "📍 Check Out",
            key="field_checkout"
        ):

            check_out(
                employee_code,
                work_date
            )

            st.success(
                "Check Out thành công"
            )

            st.rerun()
            
def show_summary(
    employee_code,
    work_date
):

    summary = get_summary(
        employee_code,
        work_date
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Tổng",
        summary["total"]
    )

    col2.metric(
        "Hoàn thành",
        summary["completed"]
    )

    col3.metric(
        "Tiến độ",
        f'{summary["percent"]}%'
    )

    st.progress(
        summary["percent"]/100
    )
    
def add_task_form(
    employee_code,
    work_date
):

    st.subheader("➕ Thêm công việc")

    task_name = st.text_input(
        "Tên công việc",
        key="field_task_name"
    )

    description = st.text_area(
        "Mô tả",
        key="field_description"
    )

    note = st.text_area(
        "Ghi chú",
        key="field_note"
    )

    if st.button(
        "💾 Lưu công việc",
        key="field_save"
    ):

        if task_name == "":

            st.warning(
                "Nhập tên công việc"
            )

            return

        add_task(
            employee_code,
            work_date,
            task_name,
            description,
            note
        )

        st.success(
            "Đã thêm công việc"
        )

        st.rerun()
        
def show_task_table(
    employee_code,
    work_date
):

    st.subheader("📋 Danh sách công việc")

    df = get_today_tasks(
        employee_code,
        work_date
    )

    if df.empty:

        st.info(
            "Chưa có công việc."
        )

        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    task_id = st.selectbox(
        "Chọn công việc",
        df["ID"].tolist(),
        key="field_task_id"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "✔ Hoàn thành",
            key="complete_task"
        ):

            complete_task(
                task_id
            )

            st.success(
                "Đã hoàn thành công việc."
            )

            st.rerun()

    with col2:

        if st.button(
            "✏ Sửa",
            key="edit_task"
        ):

            edit_task_form(
                task_id
            )

    with col3:

        if st.button(
            "🗑 Xóa",
            key="delete_task"
        ):

            delete_task(
                task_id
            )

            st.success(
                "Đã xóa công việc."
            )

            st.rerun()
            
            
def edit_task_form(task_id):

    task = get_task_by_id(task_id)

    if task is None:

        st.error(
            "Không tìm thấy công việc."
        )

        return

    st.divider()

    st.subheader("✏ Sửa công việc")

    task_name = st.text_input(
        "Tên công việc",
        value=task["task_name"],
        key=f"edit_name_{task_id}"
    )

    description = st.text_area(
        "Mô tả",
        value=task["description"],
        key=f"edit_description_{task_id}"
    )

    note = st.text_area(
        "Ghi chú",
        value=task["note"],
        key=f"edit_note_{task_id}"
    )

    if st.button(
        "💾 Cập nhật",
        key=f"save_task_{task_id}"
    ):

        update_task(
            task_id,
            task_name,
            description,
            note
        )

        st.success(
            "Đã cập nhật công việc."
        )

        st.rerun()