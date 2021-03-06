import base64, sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

def prep_SMTPemail_body(FILEPATH, SENDER, SUBJECT, html=None):

    print(" Prepping SMTP email body")

    subject = SUBJECT
    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['Subject'] = subject

    if html:
        part = MIMEMultipart('alternative')
        msg.attach(part)
        msg.attach(MIMEText(html, 'html'))
    elif html == None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(FILEPATH, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=str(FILEPATH.name))
        msg.attach(part)
        msg.attach(MIMEText('OCI SMTP Email: ' +  subject, 'plain'))
    
    
    return msg

## Bugged // fix it
def prep_sg_email(FILEPATH, SENDER, RECEPIENT, SUBJECT, HTML):

    ## templates and automation

    print(" Prepping SendGrid email")

    message = Mail(
        from_email=SENDER,
        to_emails=RECEPIENT,
        subject=SUBJECT,
        html_content=HTML
    )

    with open(FILEPATH, 'rb') as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(str(FILEPATH)),
        FileType(file_type=MIMEMultipart('alternative')),
        Disposition('attachment')
    )
    message.attachment = attachedFile

    return message