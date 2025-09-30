# scripts/send_email.py
import os
import smtplib
from email.message import EmailMessage
import sys

def get_env_var(name, default=None, required=False):
    """Pega variável de ambiente, com fallback e checagem de obrigatoriedade."""
    value = os.getenv(name, default)
    if required and not value:
        print(f"Error: Environment variable {name} is required but not set or empty.")
        sys.exit(1)
    return value

def main():
    # Pegar variáveis de ambiente
    RECIPIENT = get_env_var("RECIPIENT", required=True)
    SMTP_HOST = get_env_var("SMTP_HOST", required=True)
    SMTP_PORT = get_env_var("SMTP_PORT", "587")
    SMTP_USER = get_env_var("SMTP_USER", default=None)
    SMTP_PASS = get_env_var("SMTP_PASS", default=None)
    PIPELINE_MSG = get_env_var("PIPELINE_MSG", "Pipeline executado!")

    # Converter porta para inteiro
    try:
        SMTP_PORT = int(SMTP_PORT)
    except ValueError:
        print(f"Error: SMTP_PORT must be an integer, got '{SMTP_PORT}'")
        sys.exit(1)

    # Criar mensagem
    msg = EmailMessage()
    msg["From"] = SMTP_USER if SMTP_USER else "no-reply@example.com"
    msg["To"] = RECIPIENT
    msg["Subject"] = "CI Pipeline Notification"
    msg.set_content(f"{PIPELINE_MSG}\n\nThis is an automated message from GitHub Actions.")

    # Enviar email
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            if SMTP_USER and SMTP_PASS:
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
        raise

if __name__ == "__main__":
    main()
