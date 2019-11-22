import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from app.models import User

# Email you want to send the update from (only works with gmail)
fromEmail = 'superpi360@gmail.com'
# You can generate an app password here to avoid storing your password in plain text
# https://support.google.com/accounts/answer/185833?hl=en
fromEmailPassword = 'internetofthings'

# Email you want to send the update to
def getToEmails():
    users = User.query.all()
    return [u.email for u in users]

def sendEmail(image):
    for toEmail in getToEmails():
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = 'Security Update'
        msgRoot['From'] = fromEmail
        msgRoot['To'] = toEmail
        msgRoot.preamble = 'Raspberry pi security camera update'

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        msgText = MIMEText('Smart security cam found object')
        msgAlternative.attach(msgText)

        msgText = MIMEText('<img src="cid:image1">', 'html')
        msgAlternative.attach(msgText)

        msgImage = MIMEImage(image)
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(fromEmail, fromEmailPassword)
        smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
        smtp.quit()