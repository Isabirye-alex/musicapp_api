import resend
from app.core.config import settings
from datetime import datetime

resend.api_key = settings.RESEND_API_KEY

year = datetime.now().year


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
                <a href="https://musicapp-web.vercel.app" style="display: inline-block; background: #4f46e5; color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px;">Visit Music App</a>
              </p>
              <p style="color: #64748b; font-size: 14px;">If you didn't create this account, please contact support immediately.</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 24px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0;">
                 &copy; {year} Atlas-Music. All rights reserved.
        </td>
          </tr>
        </table>
      </body>
    </html>
    """


async def send_registration_email(email: str, first_name: str, last_name: str) -> None:
    resend.Emails.send(
        {
            "from": f"{settings.MAIL_FROM_NAME} <onboarding@resend.dev>",
            "to": email,
            "subject": "Welcome to Music App",
            "html": _render_registration_html(first_name, last_name),
        }
    )
