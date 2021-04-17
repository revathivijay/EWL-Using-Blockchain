# import os
# import secrets
# from Portal import app
# from flask import Flask, session, escape, render_template, url_for, flash, redirect, request
# from werkzeug import url_encode
from bson.objectid import ObjectId
from Portal.forms import SubmitResearchWork, VerifyReport, LoginForm, UpdateResearchWork, VerifyPublication, CreateJob
from Portal.__init__ import csv_file

from werkzeug.utils import secure_filename
import hashlib  # for SHA512
from flask_login import login_user, current_user, logout_user, login_required
# from sqlalchemy.orm import Session
import requests
import random

import os
import shutil
from bson.objectid import ObjectId

from bson import json_util
from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify, flash
import pandas

from flask_pymongo import PyMongo, MongoClient
import bcrypt

from flask import Flask, render_template, request
import os.path

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'earn_while_learn'
app.config['STATIC_FOLDER'] = '/Portal/static/'
app.config[
	'MONGO_URI'] = 'mongodb+srv://taklu:taklu@cluster0.cut8t.mongodb.net/earn_while_learn?retryWrites=true&w=majority'
app.secret_key = 'hi'

mongo = PyMongo(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print(APP_ROOT)


@app.route('/register', methods=['POST', 'GET'])
def register():
	form = LoginForm(request.form)
	if 'username' in session:
		print("IN Session")
		return redirect('/')

	if request.method == 'POST':
		print("using db")
		users = mongo.db.students
		user_id = request.form.get('id')
		user_email = request.form.get('email')
		print(user_id, user_email)

		print("search for user")
		existing_user = users.find_one({'id': user_id})
		if existing_user is None:
			print("user doesn't exist")
			hashpass = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())
			users.insert(
				{'id': user_id,
				 'email': user_email,
				 'password': hashpass})

			session['username'] = "Eshita"

			print('go home')
			return redirect('/')

		print('user exists')
		return render_template('register.html', msg="The username is taken, please enter a different username",
							   form=form)

	print('send to signup')
	return render_template('register.html', msg="", form=form)


@app.route('/register_staff', methods=['POST', 'GET'])
def register_staff():
	form = LoginForm(request.form)
	if 'username' in session:
		print("IN Session")
		return redirect('/')

	if request.method == 'POST':
		print("using db")
		users = mongo.db.staff
		user_id = request.form.get('id')
		user_email = request.form.get('email')
		print(user_id, user_email)

		print("search for user")
		existing_user = users.find_one({'id': user_id})
		if existing_user is None:
			print("user doesn't exist")
			hashpass = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())
			users.insert(
				{'id': user_id,
				 'email': user_email,
				 'password': hashpass})

			session['username'] = "Prof. Murli"

			print('go home')
			return redirect('/')

		print('user exists')
		return render_template('register_staff.html', msg="The username is taken, please enter a different username",
							   form=form)

	print('send to signup')
	return render_template('register_staff.html', msg="", form=form)


@app.route('/add_project', methods=['POST', 'GET'])
def add_project():
	print("In /add_project")
	submit_work_form = SubmitResearchWork(request.form)
	update_work_form = UpdateResearchWork(request.form)
	# if 'username' not in session:
	# 	print("IN Session")
	# 	return redirect('/')

	if request.method == 'POST':
		print("using db")
		research = mongo.db.research
		user_id_students = request.form.get('students')
		user_id_staff = request.form.get('staff')
		project_topic = request.form.get('topic')
		departments_involved = request.form.get('departments')
		print(user_id_students, user_id_staff, project_topic, departments_involved)

		if user_id_students is not None:
			print("#### inserting project ####")
			research.insert(
				{'students': user_id_students.split(","),
				 'staff': user_id_staff.split(","),
				 'topic': project_topic,
				 'departments': departments_involved.split(","),
				 'isPublished': False,
				 'publicationDOI': None,
				 'publicationJournal': None
				 }
			)

			print('Project inserted!')
			my_projects, topic_list, file_lists = get_project_lists()
			total = len(my_projects)

			return render_template('add_project.html', msg="", submit_work_form=submit_work_form,
								   update_work_form=update_work_form, my_projects=my_projects, topic_list=topic_list,
								   file_lists=file_lists, total=total)
	else:
		return render_template('add_project.html', msg="", submit_work_form=submit_work_form,
							   update_work_form=update_work_form, my_projects=[], topic_list=[],
							   file_lists=[], total=0)


@app.route('/update_project/<id>', methods=['POST', 'GET'])
def update_project(id):
	# target = os.path.join(APP_ROOT, 'static/documents')  # folder path
	# print(target)
	# if not os.path.isdir(target):
	# 	os.mkdir(target)  # create folder if not exits
	#
	# files = []
	# for upload in request.files.getlist("Document"):  # multiple image handle
	# 	filename = secure_filename(upload.filename)
	# 	destination = "/".join([target, filename])
	# 	upload.save(destination)
	# 	# research.insert({'file_list': filename})
	# 	print(filename, "ho gayi upload")
	# 	files.append({filename: False})
	# 	break

	project = mongo.db.research.find_one({"_id": ObjectId(id)})
	# if 'file_list' in project:
	# 	file_list = project["file_list"]
	# 	file_list.append(files[0])
	# else:
	# 	file_list = [files[0]]
	# mongo.db.research.update({"_id": id}, {"$set": {"file_list": file_list}})
	#
	print(project)
	# return render_template('update_project')
	return redirect('/add_project')


@app.route('/view_projects')
def view_projects():
	if 'id' in session:
		print(session['id'])
		print(session['username'])
	s_id = session['id'] if session['id'] else ""
	s_username = session['username'] if session['username'] else ""
	projects = get_student_projects(s_id, s_username)
	print(projects)
	return render_template('view_projects.html', projects=projects)

def get_student_projects(s_id, s_username):
	print("In get student projects")
	research_db = mongo.db.research
	projects = []
	for document in research_db.find():
		if s_id in document['students'] or s_username in document['students']:
			print(document)
			projects.append(document)
			# # projects.append([document['topic'], document['students'], document['staff'], document['departments']])
			# if 'filelist' in document:
			# 	projects.append([document['topic'], document['students'], document['staff'], document['departments'], document['filelist']])
			# 	print("Yes")
			# else:
			# 	projects.append([document['topic'], document['students'], document['staff'], document['departments']])
			# 	print("No")
	return projects

@app.route('/verify_report/<p_id>/<report_name>', methods=['GET', 'POST'])
def verify_report(p_id, report_name):
	gradedReports = mongo.db.gradedReports
	research = mongo.db.research
	project = research.find_one({"_id": ObjectId(p_id)})
	topic = project['topic']
	form = VerifyReport(request.form)
	if form.is_submitted():
		gradedReports.update_one({"projectID": p_id, "reportName": report_name}, {
			"$set": {"effort": form.effort.data, "relevance": form.relevance.data, "novelty": form.novelty.data}})
		project['file_list'][report_name] = True
		research.update_one({"_id": ObjectId(p_id)}, {"$set": {"file_list": project['file_list']}})
		return redirect("/teacher_dashboard")

	return render_template('verify_report.html', topic=topic, form=form)


@app.route('/verify_publication/<p_id>', methods=['GET', 'POST'])
def verify_publication(p_id):
	research = mongo.db.research
	project = research.find_one({"_id": ObjectId(p_id)})
	topic = project['topic']
	doi = project['publicationDOI']
	publicationJournal = project['publicationJournal']
	publicationJournal = "ARCHIVES OF COMPUTATIONAL METHODS IN ENGINEERING"

	form = VerifyPublication(request.form)

	if form.is_submitted():
		if 'verify' in request.form:

			research.update({"topic": topic}, {"$set": {"isPublished": True}})

			impact_factor = -1
			for row in csv_file:
				if publicationJournal == row[1]:
					impact_factor = float(row[3])
					break

			if impact_factor == -1:
				impact_factor = 2  # Generic other journal

			students_ids = project['students']
			no_of_students = len(students_ids)
			each_student_impact_factor = impact_factor / no_of_students
			for student_id in students_ids:
				students = mongo.db.students
				students.update({"id": student_id}, {'$set': {"impactScore": each_student_impact_factor}})
			flash('Verification was successful!', 'success')
			return redirect('/teacher_dashboard')
		elif 'notVerify' in request.form:
			flash('Verification was not successful!', 'danger')
			return redirect('/teacher_dashboard')
	return render_template('verify_publication.html', form=form, topic=topic, publicationJournal=publicationJournal,
						   p_id=p_id, doi=doi)


def get_project_lists():
	my_projects = []
	topic_list = []
	file_lists = []
	my_id = "171071045"

	# print("getting project lists", my_id)

	projects = mongo.db.research
	project_details = projects.find({})
	for project in project_details:
		# print("************************************", project)
		students = project["students"]
		if my_id in students:
			my_projects.append(project["_id"])
			topic_list.append(project["topic"])
			if 'file_list' in project:
				file_lists.append(project["file_list"])
			else:
				file_lists.append([])
				# print('No docs uploaded')
	# print(my_projects, topic_list, file_lists)
	return my_projects, topic_list, file_lists


@app.route('/helper_login_student')
def helper_login_student():
	session['username'] = 'Revathi'
	session['id'] = '171071045'
	return redirect('/dashboard')


@app.route('/helper_login_staff')
def helper_login_staff():
	session['username'] = 'Mr. Murli'
	session['id'] = '1'
	return redirect('/')


# @app.route('/userlogin', methods=['POST', 'GET'])
# def userlogin():
#     if not Lib.isMobileBrowser(request):
#         return "Access to this site is only available through Mobile Phones and Tablets."
#
#     if 'username' in session:
#         print("IN Session")
#         return redirect('/home')
#
#     return render_template('pages/examples/login.html', msg = "")
#
# @app.route('/login', methods=['POST'])
# def login():
#     users = mongo.db.user
#     login_user = users.find_one({'username': request.form['username']})
#     print("{{{{{{{{{{{{{{{{{", request.form['username'], request.form.get('password'))
#     if login_user:
#         if bcrypt.hashpw(request.form.get('password').encode('utf-8'), login_user['password']) == login_user['password']:
#             session['username'] = request.form['username']
#             # print("((((((((((((((((((((((((", login_user['password'])
#             # session['type'] = "alumni"
#             return redirect('/home')
#
#     return  render_template('pages/examples/login.html', msg = "Invalid Username/Password")
#
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/register')


@app.route("/")
def home():
	return "HOME"


@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
	all_students, student_impact_score = displayRanklist()
	form = SubmitResearchWork(request.form)
	return render_template('index.html', title='Dashboard', form=form, all_students=all_students,
						   student_impact_score=student_impact_score, total=len(all_students))


@app.route("/teacher_dashboard", methods=['POST', 'GET'])
def teacher_dashboard():
	###TODO: get teacher_id from login
	teacher_id = '1'
	research = mongo.db.research
	all_research_projects = research.find({'staff': teacher_id})
	vr_topic_list = []
	vp_topic_list = []
	p_id_vr = []
	p_id_vp = []
	report_name_vr = []

	for project in all_research_projects:

		# Any report is not verified in a certain topic
		for file in project['file_list']:
			if project['file_list'].get(file) == False:
				vr_topic_list.append(project['topic'] + ":\t" + str(file))
				p_id_vr.append(str(project['_id']))
				report_name_vr.append(file)

		# students submitted for publication but teacher needs to verify
		if (project['isPublished'] == False and project['publicationDOI'] != None and project[
			'publicationJournal'] != None):
			vp_topic_list.append(project['topic'])
			p_id_vp.append(str(project['_id']))

	return render_template('teacher_dashboard.html', title='Dashboard', vr_topic_list=vr_topic_list, p_id_vr=p_id_vr,
						   report_name_vr=report_name_vr, total_vr=len(p_id_vr), vp_topic_list=vp_topic_list,
						   p_id_vp=p_id_vp, total_vp=len(p_id_vp))


@app.route("/ranklist", methods=['GET', 'POST'])
def ranklist():
	return render_template("ranklist.html")


def displayRanklist():
	students = mongo.db.students
	cursor = students.find({"impactScore": {"$gt": 0}})
	all_students = []
	student_score = []
	for document in cursor:
		all_students.append(document['id'])
		student_score.append(document['impactScore'])
	return all_students, student_score


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#
#         #modified to use SHA512
#
#         s = 0
#         for char in (form.password.data):
#             a = ord(char)
#             s = s+a
#         now_hash = (str)((hashlib.sha512((str(s).encode('utf-8'))+((form.password.data).encode('utf-8')))).hexdigest())
#         #if user and bcrypt.check_password_hash(user.password, form.password.data):
#         if (user and (user.password==now_hash)):
#
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('dashboard'))
#
#         else:
#             print('nahin hua login')
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#
#     else:
#         print('ho gaya')
#     return render_template('login.html', title='Login', form=form)
#
#
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('login'))
#
#
#
#
#
# @app.route("/dashboard", methods= ['POST', 'GET'])
# def dashboard():
#     # to be added to dashboard:
#     # <div class="col s6">
#     #     {% for papers in studentSubmissions %}
#     #         <a href = "{{ url_for('static', filename= student.ID + organizer.photo1) }}"> <img class="circle responive-img account-img" src="{{ photo1 }}"> </a>
#     #     { % endfor %}
#     # </div>
#     return render_template('dashboard.html', title='Dashboard')


@app.route("/get_open_jobs", methods=["POST", "GET"])
def get_open_jobs():
	jobs_ = mongo.db.jobs
	jobs = jobs_.find({})

	# add condition for displaying only jobs w unfilled vacancies
	L_title = []
	L_description = []
	L_vacancies = []
	L_id = []
	for job in jobs:
		print(job["title"], job["description"], job["vacancies"])
		title, description, vacancies, id = job["title"], job["description"], job["vacancies"], job["id"]
		L_title.append(title)
		L_description.append(description)
		L_vacancies.append(vacancies)
		L_id.append(id)
	total = len(L_title)

	return render_template('get_open_jobs.html', title_list=L_title, description_list=L_description,
						   vacancies_list=L_vacancies, L_id=L_id, total=total)


# Get candidates
@app.route("/get_candidates/<job_id>", methods=["POST", "GET"])
def get_candidates(job_id):
	jobs_ = mongo.db.jobs
	job = jobs_.find_one({"id": job_id})
	job_title = job["title"]
	job_vacancies = job["vacancies"]

	candidates = job["candidates"]
	candidates_db = mongo.db.students

	L_id = []
	L_name = []
	L_description = []
	L_resume = []

	for candidate_id in candidates:
		candidate = candidates_db.find_one({"id": candidate_id})

		print(candidate["id"], candidate["name"], candidate["description"], candidate["resume"])
		id, name, description, resume = candidate["id"], candidate["name"], candidate["description"], candidate[
			"resume"]

		L_id.append(id)
		L_name.append(name)
		L_description.append(description)
		L_resume.append(resume)

		total = len(L_id)

	return render_template('get_candidates.html', id_list=L_id, name_list=L_name, description_list=L_description,
						   resume_list=L_resume, total=total, title=job_title, vacancies=job_vacancies, job_id=job_id)


# Apply for job
@app.route("/apply_for_job/<job_id>", methods=["POST", "GET"])
# by student applying for jobs
def apply_for_job(job_id):
	candidate_id = 1  # student id who has logged in
	# print()
	job = mongo.db.jobs.find_one({"id": int(job_id)})
	candidates = []
	if "candidates" in job:
		candidates = job['candidates']
	candidates.append(candidate_id)

	mongo.db.jobs.update_one({"id": int(job_id)}, {'$set': {'candidates': candidates}})

	# add a condition later to prevent appending/applying more than once if already applied
	flash('You have succesfully applied for ' + job[
		'title'] + '. You will be notified regarding your application status shortly. ', 'success')
	return redirect(url_for('get_open_jobs'))


# return render_template('get_open_jobs.html', candidates=job["candidates"])


# Add candidate (by staff)
@app.route("/add_candidate/<job_id>/<student_id>", methods=["POST", "GET"])
# for staff alloting a job to the student
def add_candidate(job_id, student_id):
	candidate_id = student_id
	# print()
	job = mongo.db.jobs.find_one({"id": job_id})
	if "candidates" in job:
		job["candidates"].append(candidate_id)
	else:
		job["candidates"] = [candidate_id]
		job["vacancies"] = job["vacancies"] - 1
	return redirect(url_for('get_candidates', job_id=job_id))


# Create job
@app.route("/create_job", methods=["POST", "GET"])
def create_job():
	form = CreateJob(request.form)

	if form.is_submitted():
		print("using db")
		jobs = mongo.db.jobs
		id = jobs.count()
		title = request.form.get('title')
		description = request.form.get('description')
		duration = request.form.get('duration')
		vacancies = request.form.get('vacancies')
		jobs.insert(
			{"id": id, "title": title, "description": description, "duration": duration, "vacancies": vacancies})
		print("job added")
		return redirect("/get_open_jobs")
	return render_template('create_job.html', create_job_form=form)


def allocate_job(job_id):
	jobHistory = mongo.db.jobHistory
	jobs = mongo.db.jobs
	curr_job = jobs.find_one({"job_id": job_id})
	jobHistory.find({"job_id": job_id})
	if len(jobHistory) < 25:
		selected_candidates = random.sample(curr_job["candidates"], curr_job["vacancies"])
	else:
		# TODO
		selected_candidates = []
	return selected_candidates


@app.route('/grade_job/<job_id>/<candidate_id>', methods=['GET', 'POST'])
def grade_job(job_id, candidate_id):
	return render_template('verify_publication.html', form=form, topic=topic, publicationJournal=publicationJournal,
						   p_id=p_id, doi=doi)



if __name__ == '__main__':
	app.run(debug=True, port=1240)
