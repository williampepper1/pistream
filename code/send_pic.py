import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def attach_pic(file_name):
    email_user = 'superpi360@gmail.com'
    email_password = 'internetofthing!'
    email_send = ['th.kim9112@gmail.com']

    # Subject of eamil
    subject = 'Sending picture of streaming video'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = ", ".join(email_send)
    msg['Subject'] = subject

    # 본문 내용 입력
    body = 'Attaching files'
    msg.attach(MIMEText(body,'plain'))

    ############### Attaching file ########################
    filename= file_name
    attachment  =open(filename,'rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= " + filename)
    msg.attach(part)
    #######################################################

    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()
