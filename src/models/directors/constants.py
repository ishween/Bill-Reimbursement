import string
import random
import smtplib
from email.mime.text import MIMEText

COLLECTION = "director"


def send_email(email, password):
    # to send mail
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('ishweenk999@gmail.com', 'isha@1999')
    txt = "You have been added for bill reimbursement:" \
          "'Your username: {} and password: {}".format(email, password)
    me = 'ishweenk999@gmail.com'
    msg = MIMEText(txt)
    msg['Subject'] = "You have been added for Bill Reimbursement"
    msg['From'] = me
    s.sendmail(me, email, msg.as_string())


def password_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    # to generate password for initial entry of the managers
    return ''.join(random.choice(chars) for _ in range(size))