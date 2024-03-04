import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from src.settings import EmailEnv


def create_email_attachments(message: MIMEMultipart, attachment_file_paths: list[str] = None) -> MIMEMultipart:
    if not attachment_file_paths:
        return message
    for file_path in attachment_file_paths:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        file_name = Path(file_path).name
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )

        message.attach(part)
    return message


def send_email(subject, body: str, attachment_file_paths: list[str] = None):
    message = MIMEMultipart()
    message["From"] = EmailEnv.SENDER_EMAIL
    message["To"] = EmailEnv.RECEIVERS_EMAIL
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    message = create_email_attachments(message, attachment_file_paths)

    text = message.as_string()

    with smtplib.SMTP(EmailEnv.SMTP_HOST, EmailEnv.SMTP_PORT) as server:
        server.login(EmailEnv.SENDER_EMAIL, EmailEnv.SENDER_PASSWORD)
        server.sendmail(EmailEnv.SENDER_EMAIL, EmailEnv.RECEIVERS_EMAIL, text)


if __name__ == '__main__':
    send_email(subject="test subject", body="test body", attachment_file_paths=[])
