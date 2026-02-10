import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()
import os
sender_email=os.environ["SENDER_EMAIL"]
app_password=os.environ["APP_PASSWORD"]

# Email details
def send_email(receiver_email: str, subject: str, content: str) -> str:
    """Send an email to the specified receiver with the given subject and content."""
    # Create email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(content, "plain"))

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)

    return "Email sent successfully!"

