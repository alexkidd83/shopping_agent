"""
Stubbed email utility for sending reports or notifications to the user.
In a real application, you would integrate with an email service such
as SMTP, SendGrid or AWS SES.  Credentials and recipients would be
configured via environment variables or configuration files.
"""

from typing import List


def send_email(subject: str, body: str, recipients: List[str]) -> None:
    """
    Pretend to send an email by printing the contents to the console.
    Replace this with calls to a real email service when ready.
    """
    print(f"\n=== Email Sent ===")
    print(f"To: {', '.join(recipients)}")
    print(f"Subject: {subject}")
    print("Body:\n" + body)
