# read scores from each
from Portal.routes import  app
from flask_pymongo import PyMongo, MongoClient

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/earn_while_learn'
app.secret_key = 'hi'

mongo = PyMongo(app)
research = mongo.db.research
research.update_many({}, {"$unset": {"degree":"B-Tech"}})

cursor = research.find({})
#one time insertion
for document in cursor:
      print(document)