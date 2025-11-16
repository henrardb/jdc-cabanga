import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import os

def send_daily_report(report_content: str, subject: str = "JDC Cabanga Report"):
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = os.getenv("SMTP_PORT")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    print(f"DEBUG: {SMTP_SERVER}, {SMTP_PORT}, {SENDER_EMAIL},{RECEIVER_EMAIL},{SMTP_PASSWORD}")

    if not all([SENDER_EMAIL, RECEIVER_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT]):
        print("Environment variables missing")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subject
    msg['To'] = RECEIVER_EMAIL
    msg.attach(MIMEText(report_content, "plain"))

    server = None

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SMTP_PASSWORD)

            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("Email sent")
    except Exception as e:
        print(f"Error while sending: {e}")
