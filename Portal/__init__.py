from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import csv


app = Flask(__name__)

# Mongo config here 
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from Portal import routes
csv_file = csv.reader(open('./../2018JournalImpactFactor.csv', "r"), delimiter=",")