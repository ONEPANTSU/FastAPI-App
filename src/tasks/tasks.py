import smtplib
from email.message import EmailMessage

from celery import Celery

from src.config import (
    CACHE_HOST,
    CACHE_PORT,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)

celery = Celery("tasks", broker=f"redis://{CACHE_HOST}:{CACHE_PORT}")


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email["Subject"] = "Soft Message: Dashboard"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        "<div>"
        f'<h1 style="color:SlateGray;">Hello, {username}, this is a Soft Message for You 🍌</h1>'
        '<img src="https://i.pinimg.com/originals/82/87/7b/82877b2fc130753ca669e0f150c73b84.jpg" '
        'width="600">'
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username=username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
