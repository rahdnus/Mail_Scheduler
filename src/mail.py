import smtplib
import ssl
from email.message import EmailMessage
from flask import url_for,Flask, request, render_template,redirect
from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import date, datetime

email_sender = 'rahdnus119@gmail.com'
email_password = 'ftnecmsombzteuti'

app = Flask(__name__)

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
sched.start()

@app.route('/' )
def home():
    return render_template("Home.html")

@app.route('/', methods =["POST"])
def choice():
    if request.method == "POST":
        subjectchoice=request.form.get("Subject")
        if subjectchoice=="Birthday":
            return redirect(url_for("bform"), code=307)
        elif subjectchoice=="Anniversary":
            return redirect(url_for("aform"), code=307)

@app.route('/birthday',methods=["GET","POST"])
def bform():
    if request.method == "GET":
        email_receiver = request.args.get('recipientMail')
        name = request.args.get('name')
        age = request.args.get('age')
        print(age)
        time=request.args.get('time')
        time=time[0:10]+" "+time[11:]+":00"
        if len(time)<18 or name=="" or age==None:
            return render_template("Form.html",choice="Birthday")
        subject = f'Happy Birthday {name}!'
        body = f"""
        Many More Happy Returns of the Day {name}
        Congrats on your {age+numpost(int(age))} birthday
        """
        print(time)
        sched.add_job(lambda:sendMail(email_receiver,subject,body),'date',run_date = time )
        return render_template("End.html")
    return render_template("Form.html",choice="Birthday")

@app.route('/anniversary',methods=["GET","POST"])
def aform():
    if request.method == "GET":
        email_wife= request.args.get('recipientHusbandMail')
        email_husband= request.args.get('recipientWifeMail')
        name_husband = request.args.get('hus')
        name_wife = request.args.get('wife')
        years = request.args.get('years')
        time=request.args.get('time')
        time=time[0:10]+" "+time[11:]+":00"
        print(time)
        subject = f'Happy Wedding Anniversary {name_husband} and {name_wife}!'
        body = f"""
        Many More Happy Returns of the Day {name_husband} and {name_wife}
        Congrats on your {years+numpost(int(years))} anniversary
        """
        sched.add_job(lambda:[sendMail(email_husband,subject,body),sendMail(email_wife,subject,body)],'date',run_date = time )
        return render_template("End.html")
    return render_template("Form.html",choice="Anniversary")

def numpost(num):
    low=num%10
    if low==1:
        return "st"
    elif low==2:
        return "nd"
    elif low==3:
        return "rd"
    else:
        return "th"