from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	id = StringField('ID Number', validators=[])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

class SubmitResearchWork(FlaskForm):
	students = StringField('students', validators=[DataRequired()])
	staff = StringField('staff', validators=[DataRequired()])
	topic = StringField('topic', validators=[DataRequired()])
	departments = StringField('departments', validators=[DataRequired()])
	Document = FileField('Document',validators=[FileAllowed(['.docx', '.pdf', '.txt'])])
	submit = SubmitField('Add')

class UpdateResearchWork(FlaskForm):
	updatedDocument = FileField('Document',validators=[FileAllowed(['.docx', '.pdf', '.txt'])])
	publishedStatus = SelectField('Current Status', choices=[('P','Published'), ('S','Submitted'),('N', 'Not submitted, still working')])
	publication = StringField('Journal Name')
	DOI = IntegerField('DOI')
	update = SubmitField('Update')

class ReviewSubmission(FlaskForm):
	scale = [(1, 'Non-existent'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')]
	effort = SelectField('Effort', choices=scale, validators=[Required()])
	novelty = SelectField('Novelty', choices=scale, validators=[Required()])
	relevance = SelectField('Relevance', choices=scale, validators=[Required()])
	publishedStatus = SelectField('Current Status', choices=[('P','Published'), ('S','Submitted'),('N', 'Not submitted, still working')])
	verify = SubmitField('Verified')
