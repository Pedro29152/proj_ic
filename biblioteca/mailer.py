import smtplib
from os import getenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_message(assunto, receiver_email, html_message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = getenv('MAILER_SENDER_EMAIL')
    msg['To'] = receiver_email
    htmlPart = MIMEText(html_message, 'html')
    msg.attach(htmlPart)
    return msg.as_string()

def send_email(receiver_email, message):
    smtp_server = getenv('MAILER_SMTP_SERVER')
    password = getenv('MAILER_PASSWORD')
    sender_email = getenv('MAILER_SENDER_EMAIL')

    with smtplib.SMTP(smtp_server, 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        a = server.sendmail(sender_email, receiver_email, message)
