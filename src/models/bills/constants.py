import smtplib
from email.mime.text import MIMEText

COLLECTION = "bills"


def send_email(email, status):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('ishweenk999@gmail.com', 'isha@1999')
    txt = "Your bill status is updated: {}".format(status)
    me = 'ishweenk999@gmail.com'
    msg = MIMEText(txt)
    msg['Subject'] = 'Your bill status has been updated'
    msg['From'] = me
    s.sendmail(me, email, msg.as_string())