from typing import Dict, List
import os


def get_body(data: List[Dict] = None):
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
    return text


def send_os_mail(receiver_email: str, data: List = None, subject: str = None):
    os.system("echo '%s' | mailx -s '%s' %s" % (get_body(), subject, receiver_email))
    pass
