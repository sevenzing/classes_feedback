import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from classes_feedback.settings import EMAIL_PASSWORD
from classes_feedback.settings import EMAIL_LOGIN


def send_password(email: str, password: str):
    server = 'smtp.yandex.ru'
    user = EMAIL_LOGIN
    email_password = EMAIL_PASSWORD
    recipients = [email]
    sender = 'Innopolis Feedback app'
    subject = 'Innopolis Feedback registration'
    text = 'Hello! Your requested registration via telegram to Innopolis Feedback app! ' \
           'Your code for access to bot is: ' + password + ' .Please, enter it to the bot. Best wishes!'
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    # filepath = "/var/log/maillog"
    # basename = os.path.bgasename(filepath)
    # filesize = os.path.getsize(filepath)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Innpolis.Feedback <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')
    # part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    # part_file.set_payload(open(filepath, "rb").read())
    # part_file.add_header('Content-Description', basename)
    # part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    # encoders.encode_base64(part_file)

    msg.attach(part_text)
    msg.attach(part_html)
    # msg.attach(part_file)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, emпail_password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
    return

