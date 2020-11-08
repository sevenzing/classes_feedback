import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

from modules.surveys.config import EMAIL_LOGIN, EMAIL_MESSAGE, EMAIL_PASSWORD


def send_password(email: str, password: str):
    """
    Send password to the specified email
    :param email: Email of the student to send password to
    :param password: Verification code for the telegram authorization
    :return: None
    """
    server = 'smtp.yandex.ru'
    user = EMAIL_LOGIN
    email_password = EMAIL_PASSWORD
    recipients = [email]
    sender = user
    subject = 'Innopolis Feedback registration'
    text = EMAIL_MESSAGE % password
    html = '<html><head></head><body><p>' + text + '</p></body></html>'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Innopolis.Feedback <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())
    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')
    msg.attach(part_text)
    msg.attach(part_html)
    mail = smtplib.SMTP_SSL(server)
    mail.login(user, email_password)
    t = mail.sendmail(sender, recipients, msg.as_string())
    logging.debug(f"recipients: {recipients}, {t}")
    mail.quit()
