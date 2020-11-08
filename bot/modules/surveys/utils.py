import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from classes_feedback.settings import EMAIL_PASSWORD, EMAIL_LOGIN, EMAIL_MESSAGE


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
    sender = 'Innopolis Feedback app'
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
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()

