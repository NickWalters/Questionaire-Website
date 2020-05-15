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
	StaticForm.radioField = RadioField('radioField', coerce=int, choices=choices)
	StaticForm.submit = SubmitField('Submit')
	return StaticForm()