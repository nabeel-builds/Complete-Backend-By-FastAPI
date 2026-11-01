from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fastmail = FastMail(conf)

async def send_verification_mail(email: str, token: str):
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Please verify your email by clicking in the following link: "
            f"http://localhost:8000/verify-email?token={token}",
        subtype=MessageType.plain
    )
    await fastmail.send_message(message)



async def send_reset_password_email(email: str, token: str):
    message = MessageSchema(
            subject="Reset your password",
            recipients=[email],
            body=f"Please reset your password by clicking in the following link: "
                f"http://localhost:8000/reset-password?token={token}",
            subtype=MessageType.plain
    )
    await fastmail.send_message(message)



async def send_otp_email(email:str, otp:str):
    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is {otp}. It will expire in 10 minutes.",
        subtype=MessageType.plain
    )
    await fastmail.send_message(message)