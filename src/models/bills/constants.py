import smtplib
from email.mime.text import MIMEText

COLLECTION = "bills"


def send_email(email, reimburse, status):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('ishweenk999@gmail.com', 'isha@1999')
    if status == "accept":
        txt = "Your bill is accepted with reimbursement amount of Rs.{}".format(reimburse)
    else:
        txt = "Your bill has been rejected"
    me = 'ishweenk999@gmail.com'
    msg = MIMEText(txt)
    msg['Subject'] = 'Your bill status has been updated'
    msg['From'] = me
    s.sendmail(me, email, msg.as_string())