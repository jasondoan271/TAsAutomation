import smtplib
from email.message import EmailMessage
from email_secrets import SMTP_USER, SMTP_PASS

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(recipients, content):
    msg = EmailMessage()
    msg["Subject"] = "Daily Cyber Threat Advisory"
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg.set_content(content)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


