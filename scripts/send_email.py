# scripts/send_email.py
import os
import smtplib
from email.message import EmailMessage
import sys

RECIPIENT = os.getenv("RECIPIENT")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
PIPELINE_MSG = os.getenv("PIPELINE_MSG", "Pipeline executado!")

if not RECIPIENT:
    print("RECIPIENT not set. Exiting with error.")
    sys.exit(1)

msg = EmailMessage()
msg["From"] = SMTP_USER or "no-reply@example.com"
msg["To"] = RECIPIENT
msg["Subject"] = "CI Pipeline Notification"
msg.set_content(f"{PIPELINE_MSG}\n\nThis is an automated message from GitHub Actions.")

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print("Email sent.")
except Exception as e:
    print("Failed to send email:", e)
    # fail so action logs the error
    raise
