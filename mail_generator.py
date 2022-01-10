import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import yaml

with open('./credentials.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)


def ticket_mail(email: str, name: str, fileName: str, pnr: int):
    body = f'''Hello, {name.title()}
Please find the attachment which contains your ticket.'''

    sender = 'textacct.2001@gmail.com'
    password = data["email_password"]
    receiver = email

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = f"Ticket for PNR: {pnr}"

    message.attach(MIMEText(body, 'plain'))

    pdfname = fileName

    binary_pdf = open(pdfname, 'rb')

    payload = MIMEBase('application', 'octate-stream',
                       Name=pdfname.split("/")[2])

    payload.set_payload((binary_pdf).read())

    encoders.encode_base64(payload)

    payload.add_header('Content-Decomposition', 'attachment',
                       filename=pdfname.split("/")[2])
    message.attach(payload)

    session = smtplib.SMTP('smtp.gmail.com', 587)

    session.starttls()

    session.login(sender, password)

    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()

    print('Mail Sent')
