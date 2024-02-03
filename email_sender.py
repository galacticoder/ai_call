import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from validate_email_address import validate_email

def send_email(sender_email, sender_password, recipient_email, subject, message, attachment_path=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = sender_password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    if attachment_path:
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=file.name)
            msg.attach(attachment)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", str(e))

    finally:
        server.quit()