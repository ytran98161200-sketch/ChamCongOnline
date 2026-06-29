import streamlit as st

from field_checklist import (
    get_field_report,
    get_employee_tasks
)


def show_field_report():

    st.title("📍 Báo cáo nhân viên thị trường")

    df = get_field_report()

    if df.empty:

        st.info("Chưa có dữ liệu.")

        return

    for i, row in df.iterrows():

        title = (
            f"👤 {row['Họ tên']} | "
            f"{row['Ngày']}"
        )

        with st.expander(title):

            col1, col2, col3 = st.columns(3)

# ===========================
# Format thời gian
# ===========================

            check_in = "--"

            if row["Check In"] is not None:
                check_in = row["Check In"].strftime("%H:%M:%S")

            check_out = "--"

            if row["Check Out"] is not None:
                check_out = row["Check Out"].strftime("%H:%M:%S")

            # ===========================
            # Hiển thị
            # ===========================

            with col1:

                st.success("🟢 Check In")

                st.write(check_in)

            with col2:

                st.info("🔴 Check Out")

                st.write(check_out)

            with col3:

                total = row["Tổng CV"] if row["Tổng CV"] else 0
                completed = row["Hoàn thành"] if row["Hoàn thành"] else 0

                percent = 0

                if total > 0:
                    percent = round(completed * 100 / total)

                st.metric(
                    "Tiến độ",
                    f"{percent}%"
                )

                st.progress(percent / 100)

            st.write("**Mã nhân viên:**", row["Mã NV"])
            st.write("**Phòng ban:**", row["Phòng ban"])

            detail = get_employee_tasks(
                row["Mã NV"],
                row["Ngày"]
            )

        if detail.empty:

            st.warning("Chưa có công việc.")

        else:

            st.markdown("### 📋 Chi tiết công việc")

            for _, task in detail.iterrows():

                icon = "✅" if task["Hoàn thành"] else "⬜"

                with st.container():

                    st.write(f"{icon} **{task['Công việc']}**")

                    if task["Mô tả"]:
                        st.caption(f"📄 {task['Mô tả']}")

                    if task["Ghi chú"]:
                        st.caption(f"📝 {task['Ghi chú']}")

                    st.divider()