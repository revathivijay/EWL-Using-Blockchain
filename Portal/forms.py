from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, \
    SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    id = StringField('ID Number', validators=[])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class SubmitResearchWork(FlaskForm):
    students = StringField('students', validators=[DataRequired()])
    # staff = StringField('staff', validators=[DataRequired()])
    staff = SelectField('Mentor List', choices=[('0', 'Please select mentor'), ('1', 'Dr. Dhiren Patel'), ('2', 'Prof. Vaibhav Dhore'), ('3', 'Dr. Sunil Bhirud'), ('4', 'Dr. Faruk Kazi')],
                        validators=[DataRequired()])
    topic = StringField('topic', validators=[DataRequired()])
    # departments = StringField('departments', validators=[DataRequired()])
    departments = SelectField('departments', choices=[('-1', 'Please Select Department'), ('0', 'Computer Engg and IT'), ('1', 'Electrical Dept'), ('2', 'Mechanical Dept'), ('3', 'Civil Dept')],
                              validators=[DataRequired()])
    Document = FileField('Document', validators=[FileAllowed(['.pdf'])])
    submit = SubmitField('Add')

class UploadResearchReport(FlaskForm):
    Document = FileField('Document', validators=[FileAllowed(['.pdf'])])
    submit = SubmitField('Submit Report')

class UpdatePublicationDetails(FlaskForm):
    publishedStatus = SelectField('Current Status', choices=[('P', 'Published'), ('S', 'Submitted'),
                                                             ('N', 'Not submitted, still working')])
    publication = StringField('Journal Name')
    DOI = IntegerField('DOI')
    update = SubmitField('Update')

class VerifyProjectMentor(FlaskForm):
    verify = SubmitField('Verified')
    not_verify = SubmitField('Not Verified')


class VerifyReport(FlaskForm):
    scale = [(1, 'Non-existent'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')]
    effort = SelectField('Effort', choices=scale, validators=[Required()])
    novelty = SelectField('Novelty', choices=scale, validators=[Required()])
    relevance = SelectField('Relevance', choices=scale, validators=[Required()])
    publishedStatus = SelectField('Current Status', choices=[('P', 'Published'), ('S', 'Submitted'),
                                                             ('N', 'Not submitted, still working')])
    verify = SubmitField('Verified')


# class AddJobs(FlaskForm):
# 	title = StringField('Job title', validators=[DataRequired()])
# 	place = SelectField('Place', choices=[('C','Canteen'), ('I','Internet Lab'),('L', 'Library')])
# 	description = StringField('Job description', validators=[DataRequired()])
# 	vacancy = IntegerField('Vacancy', validators=[DataRequired()])
# 	add = SubmitField('Add Job')

class VerifyPublication(FlaskForm):
    topic = StringField("Topic")
    publicationJournal = StringField("Journal")
    DOI = StringField("DOI")
    verify = SubmitField('Verified')
    notVerify = SubmitField('Not Verified')


class CreateJob(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    duration = IntegerField('Duration in total hours required', validators=[DataRequired()])
    description = StringField('Job description', validators=[DataRequired()])
    vacancies = IntegerField('Vacancies', validators=[DataRequired()])
    start_date = DateField('Start Date Of Job', validators=[DataRequired()])
    createJob = SubmitField('Add Job')


class UpdateJobs(FlaskForm):
    vacancies = IntegerField('Vacancies', validators=[DataRequired()])
    acceptingApplication = SelectField('Accepting applications', choices=[('Y', 'Yes'), ('N', 'No')])
    update = SubmitField('Update Job')


class GradeJob(FlaskForm):
    scale = [(2, 'Non-existent'), (4, 'Poor'), (6,'Average'), (8, 'Good'), (10, 'Excellent')]
    grade = SelectField("How was the student's performance", choices=scale, validators=[Required()])

    submit = SubmitField('Submit')


class CreatePost(FlaskForm):
    cause = StringField("Cause for which you need the money", validators=[DataRequired()])
    description = StringField("Description")
    money = IntegerField("Amount", validators=[DataRequired()])
    endDate = DateField("Date by which the amount is needed", validators=[DataRequired()])
    submit = SubmitField("Create Post")


class MakePayment(FlaskForm):
    amount = IntegerField("Amount", validators=[DataRequired()])
    receiverID = StringField("Receiver", validators=[DataRequired()])
    submit = SubmitField("Make Payment")
