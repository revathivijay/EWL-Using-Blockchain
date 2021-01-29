# read scores from each
from Portal.routes import  app
from flask_pymongo import PyMongo, MongoClient
from bson import ObjectId

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/earn_while_learn'
app.secret_key = 'hi'

mongo = PyMongo(app)
students = mongo.db.students
research = mongo.db.research
staff = mongo.db.staff
gradedReports = mongo.db.reports
# students.update_many({}, {"$set": {"impactScore":0}})
# research.update({}, {"$unset": {"impactFactor":-1}})
# research.update({"_id":ObjectId('5fd04d720d98dceeddf66ad6')}, {"$set":{"file_list":{}}})
# research.update({"_id":ObjectId('5fd04dce0d98dceeddf66ad7')}, {"$set":{"file_list":{}}})
research.update({"_id":ObjectId('5fd335f349359305f83f9d04')}, {"$set":{"publicationDOI":"10.1145/3327960.3332389", "publicationJournal":"Future Generation Computer Systems-The International Journal of eScience", "isPublished":False}})
# cursor = research.find({})# report1 = {"projectID":"5fd335f349359305f83f9d04", "reportName":"report1.pdf", "effort": 3, "relevance":3, "novelty":3}
# gradedReports.insert_one(report1)
cursor = research.find({})
#one time insertion
for document in cursor:
      print(document)