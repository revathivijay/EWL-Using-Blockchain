# read scores from each
from Portal.routes import  app
from flask_pymongo import PyMongo, MongoClient
from bson import ObjectId

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['STATIC_FOLDER'] = '/Portal/static/'
app.config['MONGO_URI'] = 'mongodb+srv://taklu:taklu@cluster0.cut8t.mongodb.net/earn_while_learn?retryWrites=true&w=majority'
app.secret_key = 'hi'

mongo = PyMongo(app)
students = mongo.db.students
research = mongo.db.research
staff = mongo.db.staff
gradedReports = mongo.db.reports
jobs = mongo.db.jobs
jobsHistory = mongo.db.jobsHistory
temp = mongo.db.temp
# students.update_many({}, {"$set": {"impactScore":0}})
# research.update({}, {"$unset": {"impactFactor":-1}})
# research.update({"_id":ObjectId('5fd04dce0d98dceeddf66ad7')}, {"$set":{"file_list":{"report1.pdf":False}}})
# research.update({"_id":ObjectId('5fd3121c5da308971f9b2aed')}, {"$set":{"file_list":{"report1.pdf":False}}})
# research.update_one({"_id":ObjectId('5fd04dce0d98dceeddf66ad7')}, {"$set":{"staff":["1"]}})

# research.update({"_id":ObjectId('5fd335f349359305f83f9d04')}, {"$set":{"publicationDOI":"10.1145/3327960.3332389", "publicationJournal":"Future Generation Computer Systems-The International Journal of eScience", "isPublished":False}})
# # cursor = research.find({})
# report1 = {"projectID":"5fd04dce0d98dceeddf66ad7", "reportName":"report1.pdf", "effort": None, "relevance":None, "novelty":None}
# report2 = {"projectID":"5fd04dce0d98dceeddf66ad7", "reportName":"report2.pdf", "effort": None, "relevance":None, "novelty":None}
# gradedReports.insert_many([report1, report2])

# temp.insert_one({"isRitu":True})
cursor = temp.find({})
#one time insertion
for document in cursor:
	print(document)

import random



import random



import random



import random


