import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import os

def send_daily_report(
        html_content: str,
        subject: str = "JDC Cabanga: Résumé des devoirs",
        plain_fallback: str | None = None,
):

    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not all([SENDER_EMAIL, RECEIVER_EMAIL, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT]):
        print("Environment variables missing")
        return

    if plain_fallback is None:
        plain_fallback = "Your email client does not support HTML. Please view this message in an HTML-capable client."

    msg = MIMEMultipart("alternative")
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subject
    msg['To'] = RECEIVER_EMAIL

    part_text = MIMEText(plain_fallback, "plain", "utf-8")
    part_html = MIMEText(html_content, "html", "utf-8")

    msg.attach(part_text)
    msg.attach(part_html)

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("Email sent")
    except Exception as e:
        print(f"Error while sending: {e}")