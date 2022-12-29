import smtplib
import ssl
from email.message import EmailMessage
from flask import url_for,Flask
from apscheduler.schedulers.background import BackgroundScheduler

email_sender = 'rahdnus119@gmail.com'
email_password = 'ftnecmsombzteuti'
email_receiver = 'rahdnus119@gmail.com'
subject = 'Check out my new video!'
body = """
I've just published a new video on YouTube: https://youtu.be/2cZzP9DLlkg
"""

app = Flask(__name__)

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

def sendMail(email_receiver,subject,body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

sched = BackgroundScheduler(daemon=True)
sched.add_job(lambda:sendMail(email_receiver,subject,body),'interval',minutes=0.05)
sched.start()

@app.route('/')
def index():
    return 'index'


