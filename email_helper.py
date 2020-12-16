import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List

SENDER_EMAIL = "**************"
SENDER_PASSWORD = "********"


def get_body(
    receiver_email: str,
    data: List[Dict] = None,
    subject: str = "Email Reset Notification",
):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    if data:
        text = f"""\
                       Hi,
                       Please find the data {data}"""

        html = """<!DOCTYPE html><title></title><p>Hello,<p>Following is the message 
        <ul>%(somelist)s</ul><p>Thank you. """ % dict(
            somelist="\n".join(["<li> " + str(item) for item in data])
        )
        # html = f"""\
        #         <html>
        #           <body>
        #             <p>Hi,<br>
        #                Please find the data {data}<br>
        #             </p>
        #           </body>
        #         </html>
        #         """
    else:
        text = """\
                Hi,
                Your password is about to expire, please update your password"""
        html = """\
        <html>
          <body>
            <p>Hi,<br>
               Your password is about to expire, please update your password<br>
            </p>
          </body>
        </html>
        """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    return message


def send_email(receiver_email: str, data: List = None, subject: str = None):
    message = get_body(receiver_email=receiver_email, data=data, subject=subject)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())