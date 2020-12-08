from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class SubmitResearchWork(FlaskForm):
	submittedWork = FileField('Research work',validators=[FileAllowed(['.docx', '.pdf', '.txt'])])

class ReviewSubmission(FlaskForm):
	scale = [(1, 'Non-existent'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')]
	effort = SelectField('Effort', choices=scale, validators=[Required()])
	novelty = SelectField('Novelty', choices=scale, validators=[Required()])
	relevance = SelectField('Relevance', choices=scale, validators=[Required()])
