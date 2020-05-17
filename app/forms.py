from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.widgets import html_params, HTMLString
from app.models import User,Question,QuestionChoice
from email_validator import validate_email, EmailNotValidError

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('User name has been used.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email has been used.')

def StyleOneForm(choices, *args, **kwargs):
	class StaticForm(FlaskForm):
		pass
	StaticForm.radioField = RadioField('radioField', coerce=int, choices=choices)
	StaticForm.submit = SubmitField('Submit')
	return StaticForm()

def StyleTwoForm(choices, *args, **kwargs):
	class StaticForm(FlaskForm):
		pass
	#StaticForm.submitFields = [SubmitField(choice[1]) for choice in choices]
	StaticForm.len = len(choices)
	if StaticForm.len > 0: StaticForm.submitField0 = SubmitField(choices[0][1])
	if StaticForm.len > 1: StaticForm.submitField1 = SubmitField(choices[1][1])
	if StaticForm.len > 2: StaticForm.submitField2 = SubmitField(choices[2][1])
	if StaticForm.len > 3: StaticForm.submitField3 = SubmitField(choices[3][1])
	if StaticForm.len > 4: StaticForm.submitField4 = SubmitField(choices[4][1])
	if StaticForm.len > 5: StaticForm.submitField5 = SubmitField(choices[5][1])
	return StaticForm()