from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import csv
from flask_pymongo import PyMongo



# Mongo config here 


app = Flask(__name__)

app.secret_key = 'hi'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['STATIC_FOLDER'] = '/Portal/static/'
app.config[
    'MONGO_URI'] = 'mongodb+srv://taklu:taklu@cluster0.cut8t.mongodb.net/earn_while_learn?retryWrites=true&w=majority'


mongo = PyMongo(app)

from Portal.routes import *
csv_file = csv.reader(open('./2018JournalImpactFactor.csv', "r"), delimiter=",")