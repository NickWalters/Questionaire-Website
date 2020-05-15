from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
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

def StyleOneForm(*args, **kwargs):
	class StaticForm(FlaskForm):
		pass
	StaticForm.submit = SubmitField('Submit')
	if args:
		StaticForm.radioField = RadioField('radioField', coerce=int, choices=args[0])
	return StaticForm()

def StyleTwoForm(*args, **kwargs):
	class StaticForm(FlaskForm):
		pass
	if args:
		StaticForm.buttons = []
		for choice in args[0]:
			StaticForm.buttons.append(ButtonField(choice))
	return StaticForm()

#Credit https://gist.github.com/doobeh/239b1e4586c7425e5114
class ButtonWidget(object):
	"""
	Renders a multi-line text area.
	`rows` and `cols` ought to be passed as keyword args when rendering.
	"""
	input_type = 'submit'

	html_params = staticmethod(html_params)

	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		kwargs.setdefault('type', self.input_type)
		if 'value' not in kwargs:
			kwargs['value'] = field._value()

		return HTMLString('<button {params}>{label}</button>'.format(
			params=self.html_params(name=field.name, **kwargs),
			label=field.label.text)
		)

class ButtonField(StringField):
    widget = ButtonWidget()