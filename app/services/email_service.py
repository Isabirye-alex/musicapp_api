from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def _render_registration_html(first_name: str, last_name: str) -> str:
    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f6f8fb; margin: 0; padding: 0;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 32px auto; background: #ffffff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
          <tr>
            <td style="padding: 24px; text-align: center; border-bottom: 1px solid #e9edf2;">
              <h1 style="margin: 0; color: #1f2937;">Welcome to Music App</h1>
              <p style="margin: 8px 0 0; color: #64748b;">Your account has been created successfully.</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 32px; color: #334155;">
              <p>Hi <strong>{first_name} {last_name}</strong>,</p>
              <p>Thanks for registering with Music App. We're excited to have you on board.</p>
              <p style="margin: 24px 0;">
                <a href="https://your-music-app.example.com" style="display: inline-block; background: #4f46e5; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px;">Visit Music App</a>
              </p>
              <p style="color: #64748b; font-size: 14px;">If you didn't create this account, please contact support immediately.</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 24px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0;">
              &copy; {2026} Music App. All rights reserved.
            </td>
          </tr>
        </table>
      </body>
    </html>
    """


async def send_registration_email(email: str, first_name: str, last_name: str) -> None:
    if not all([settings.MAIL_SERVER, settings.MAIL_FROM, settings.MAIL_USERNAME, settings.MAIL_PASSWORD]):
        raise RuntimeError("Email settings are not fully configured.")

    message = MessageSchema(
        subject="Welcome to Music App",
        recipients=[email],
        body=_render_registration_html(first_name, last_name),
        subtype=MessageType.html,
    )

    fm = FastMail(mail_config)
    await fm.send_message(message)
