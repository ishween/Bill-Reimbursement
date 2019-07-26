import smtplib
from email.mime.text import MIMEText
from src.config import EMAIL, PASSWORD

COLLECTION = "bills"


def send_email(email, reimburse, status):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(EMAIL, PASSWORD)
    if status == "accept":
        txt = "Your bill is accepted with reimbursement amount of Rs.{}".format(reimburse)
    else:
        txt = "Your bill has been rejected"
    me = EMAIL
    msg = MIMEText(txt)
    msg['Subject'] = 'Your bill status has been updated'
    msg['From'] = me
    s.sendmail(me, email, msg.as_string())