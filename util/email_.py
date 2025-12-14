from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import os, random

async def generate_otp(length: int = 6) -> str:
    digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    otp = ''.join(random.choices(digits, k=length))
    return otp
    
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_USER"),
    MAIL_PORT=int(os.getenv("SMTP_PORT")),
    MAIL_SERVER=os.getenv("SMTP_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email_async(to_, from_, subject_, body_):

    message = MessageSchema(
        subject=subject_,
        sender=from_,
        recipients=[to_],
        body=body_,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)