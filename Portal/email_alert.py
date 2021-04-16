import smtplib
from Portal.routes import app
from flask_pymongo import PyMongo, MongoClient
from bson import ObjectId
from routes import mongo

# LOGIN CREDENTIALS
gmail_user = 'testvjchain@gmail.com'
gmail_password = 'vjti@123'

# FIXED VARIABLES
DEFAULT_SUBJECT = "Reminder for Upcoming Project Deadline"
rev_email = 'revathivijay99@gmail.com'
ritu_email = 'ritugala13@gmail.com'


def send_email(sender, pwd, user_id, subject=DEFAULT_SUBJECT):

    # getting project info from db
    project = mongo.db.research.find_one({"_id": ObjectId(user_id)})
    topic = project['topic']
    mentors = project['staff']
    students_in_project = project['students']
    recipients = []

    # getting student email IDs
    for student in students_in_project:
        student_details = mongo.db.students.find_one({"id": student})
        recipients.append(student_details['email'])

    # date = project['start_date']  # to be added
    date = '10 Apr 2021'

    # setting up email parameters
    FROM = sender
    TO = recipients if isinstance(recipients, list) else [recipients]
    SUBJECT = subject

    # construct body of email
    TEXT = f'''Your project titled "{topic}" under the mentor(s) {", ".join(mentors)} has an upcoming deadline of {date}. Please submit your biweekly report before this deadline.'''

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


#TODO: WRITE TRIGGER FOR THIS FUNCTION
send_email(gmail_user, gmail_password, '5fd04d720d98dceeddf66ad6')