import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import os,sys
from email import encoders
from email.utils import formataddr
from email.header import Header

class EmailManager():
    def SendEmail(self, to_email,subject, message, attach=None, CC=None):
        try:
            mailer_name = 'Zillow Bot'
            me = formataddr((str(Header(mailer_name, 'utf-8')),'naharry20@gmail.com'))
            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] =  subject
            msg['From'] = me


            if CC is not None:
                msg['CC'] = CC
                to_email.append(CC)

            html = message

            msg['To'] = ", ".join(to_email)
            part2 = MIMEText(html, 'html')


            msg.attach(part2)

            if attach is not None:
                for f in attach:
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload( open(f,"rb").read() )
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
                    msg.attach(part)
            mail = smtplib.SMTP('smtp.gmail.com','587')

            mail.ehlo()

            mail.starttls()
            mail.login(str('naharry20@gmail.com'), str('Abc@12345'))
            mail.sendmail(me, to_email, msg.as_string())
            mail.quit()
        except:
            import sys
            print(sys.exc_info())
            pass

