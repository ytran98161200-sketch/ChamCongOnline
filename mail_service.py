import smtplib
from email.mime.text import MIMEText
import streamlit as st


def send_email(
    to_email,
    subject,
    body
):
    try:
        sender = st.secrets["EMAIL_ADDRESS"]
        password = st.secrets["EMAIL_PASSWORD"]

        msg = MIMEText(
            body,
            "plain",
            "utf-8"
        )

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender,
            password
        )

        server.sendmail(
            sender,
            to_email,
            msg.as_string()
        )

        server.quit()

        return True

    except Exception as e:
        print("Lỗi gửi mail:", e)
        return False