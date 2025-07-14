# alert.py
import smtplib
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT

def send_email_alert(filename):
    """
    Sends an email alert indicating a fall was detected in the given video.
    """
    subject = "Fall Detected Alert"
    body = f"A fall was detected in the video file '{filename}' (Offline mode)."
    message = f"Subject: {subject}\n\n{body}"
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, message)
        server.quit()
        print(f"Alert email sent to {RECEIVER_EMAIL}")
    except Exception as e:
        print("Failed to send email alert:", e)
