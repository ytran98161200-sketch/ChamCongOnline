import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    to_email,
    subject,
    body
):
    sender_email = "your@gmail.com"
    app_password = "xxxx xxxx xxxx xxxx"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(
        MIMEText(body, "plain")
    )

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        sender_email,
        app_password
    )

    server.sendmail(
        sender_email,
        to_email,
        msg.as_string()
    )

    server.quit()