import string
import random
import smtplib
from email.mime.text import MIMEText
from src.config import EMAIL, PASSWORD

COLLECTION = "employees"


def password_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_email(email, password):
    s = smtplib.SMTP('smtp.sendgrid.net', 587)
    s.starttls()
    s.login(EMAIL, PASSWORD)
    txt = "You have been added for bill reimbursement:" \
          "Your Username: {} and password: {}".format(email, password)
    me = EMAIL
    msg = MIMEText(txt)
    msg['Subject'] = 'You have been added for Bill Reimbursment'
    msg['From'] = me
    s.sendmail(me, email, msg.as_string())
