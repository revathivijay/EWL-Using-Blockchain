import smtplib
from Portal.routes import app
from flask_pymongo import PyMongo, MongoClient
from bson import ObjectId

# LOGIN CREDENTIALS
gmail_user = 'testvjchain@gmail.com'
gmail_password = 'vjti@123'

# FIXED VARIABLES
DEFAULT_SUBJECT = "Reminder for Upcoming Project Deadline"
rev_email = 'revathivijay99@gmail.com'
ritu_email = 'ritugala13@gmail.com'

# SETTING UP MONGO
mongo = PyMongo(app)
students = mongo.db.students
research = mongo.db.research
staff = mongo.db.staff
gradedReports = mongo.db.reports
jobs = mongo.db.jobs


def send_email(sender, pwd, recipient, user_id, subject=DEFAULT_SUBJECT):

    FROM = sender
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject

    project = mongo.db.research.find_one({"_id": ObjectId(user_id)})
    topic = project['topic']
    mentor = project['faculty']  # is this correct
    # date = project['start_date']  # to be added
    date = '10 Apr 2021'

    # construct body of email
    TEXT = f'''Your project titled {topic} under mentor {mentor} has an upcoming deadline of {date}. 
        Please submit your biweekly report before this deadline.'''

    # construct message
    message = f"""From: {FROM}\nTo: {", ".join(TO)}\nSubject: {SUBJECT}\n\n{TEXT}"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print (f'Mail Sent successfully from {FROM} to {TO}')

    except:
        print ("Oops! Something went wrong. Mail not sent!")


# def trigger_send(user, project, date): ##TODO
#     if today less than 1 week away from date for user:
#         send_email(gmail_user, gmail_password, )

send_email(gmail_user, gmail_password, rev_email, '5fd335f349359305f83f9d04')