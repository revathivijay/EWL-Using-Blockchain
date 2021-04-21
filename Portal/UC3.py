# All routes for UC3
from flask import Flask
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify
from flask_pymongo import PyMongo, MongoClient
from flask import Flask, render_template, request
import os.path

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/earn_while_learn'
app.config['UPLOAD FOLDER'] = APP_ROOT+"/static/uploaded_images"
app.secret_key = 'hi'

mongo = PyMongo(app)



# Show all posts (i.e. dashboard)

def get_all_posts_information():
    posts_ = mongo.db.posts
    posts = posts_.find({})

    title_list = []
    likes_list = []
    images_list = []
    account_list = []
    for post in posts:
        print("Getting info...")
        title_list.append(post["title"])
        likes_list.append(post["likes"])
        images_list.append(post["images"])
        account_list.append(post["account"])
    return [title_list, likes_list, images_list, account_list]

@app.route("/view_posts", methods=["POST", "GET"])
def view_posts():
    if 'username' not in session:
        return "NOT ALLOWED"

    posts_information = get_all_posts_information()
    """ posts_information`
        [t0, t1, t2, t3],
        [l0, l1, l2, l3], 
        [   [im01, im02],
            [im11, im12, im13], 
            [im21, im22, im23]], 
            [im31, im32, im33]
        ] 
        [a0, a1, a2, a3]"""

    return render_template("view_posts.html", posts_information=posts_information)



# Create Post

def add_post(title, images, account):
    posts_ = mongo.db.posts
    posts_.insert({
        "title": title,
        "images": images,
        "account": account,
        "likes": 0
    })

@app.route("/create_post", methods=["POST","GET"])
def create_post():
    if 'username' not in session:
        return "NOT ALLOWED"
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        images_ = request.files.getlist("images[]")
        account = request.form.get("account")
        print(images_)

        # Saving the images
        images = []
        for image in images_:
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            images.append(image.filename)

        print(title, images, account, description)
        # add_post(title, images, account, description)

        return redirect('/view_posts')
    return render_template('create_post.html')

import requests


# Make donation

def get_port(account):
    if account!=None:
        return 9002

# @app.route("/make_payment/<account>/<receiver>/<amount>", methods=["POST", "GET"])
def make_payment(account, receiver, amount):

    # Details of the transaction
    port = 9002
    receiver = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE1NLZLYIiF43ljMulOipJNst4y40S3GxI0TUCGFM9i/4SoHN7DmwXZjvVz4IIRnQl5FLgA2tp8kyCIJY2LkZVuQ%3D%3D" #"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE1NLZLYIiF43ljMulOipJNst4y40S3GxI0TUCGFM9i/4SoHN7DmwXZjvVz4IIRnQl5FLgA2tp8kyCIJY2LkZVuQ=="
    receiver= receiver.replace("/", "_")
    amount = 100

    # Calculation of the url
    print("*****************")
    url = 'http://0.0.0.0:'+str(port)+'/make_transaction_without_wallet_page/'+account+'/'+receiver+'/'+str(amount)
    print(url)

    # Making the request
    if True:
        print("$$$$$$$$$$$$$$$$$$$$$")
        r = requests.get(url)
        print(r.text, "{{{{{{{{{{{{{")
        return r.text
    # else:
    #     print("^^^^^^^^^^^^^^^^^^^^^^^")
    #     return "POST request not made"

    # return r.text # redirect(url)

    # r = requests.get('http://0.0.0.0:8080/', '1')
    # print(r.text)
    # return 'Done'

def getBalance(wallet_address):
    url = "/checkBalance"
    balance = requests.get(url)
    return balance

def makeTransaction(reciver_key, sender_key):
    url = '/makeTransaction'
    data = {"receiver_public_key":reciver_key, "sender_public_key":sender_key, "bounty":0, "message":"Crowfunding"}
    result = requests.post(url, data)
    return result

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
