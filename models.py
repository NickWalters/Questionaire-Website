from app import db
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin

class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	admin = db.Column(db.Boolean, default=False, nullable=False) 
	password_hash = db.Column(db.String(128))

	# scores = db.relationship('Result', backref'user', lazy="dynamic")
	
	def is_admin(self):
		return self.admin

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return 'User: {}'.format(self.username)+', Admin: {}'.format(self.admin)

class Style(db.Model):
	__tablename__ = 'style'
	id = db.Column(db.Integer,primary_key=True)
	style = db.String(80)

class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))
	creator_id = db.Column(db.Integer, ForeignKey('user.id'))
	style = db.Column(db.Integer, ForeignKey('style.id'))
	questions = db.relationship('Question', backref='person', lazy=True)

	def __repr__(self):
		return '<Quiz {}>'.format(self.question)

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer,primary_key=True)
	quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'))
	question_number = db.Column(db.Integer)
	question_content = db.Column(db.String(80))
	question_choices = db.relationship('QuestionChoice', backref='person', lazy=True)
	def __repr__(self):
		return '<Question {}>'.format(self.question)

class QuestionChoice(db.Model):
	__tablename__ = 'questionChoice'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_number = db.Column(db.Integer)
	choice_content = db.Column(db.String(80))
	choice_correct = db.Column(db.Boolean)
	choice_chosen = db.relationship('UserAnswer', backref='person', lazy=True)
	
	def __repr__(self):
		return '<Choice {}>'.format(self.choice)

class UserAnswer(db.Model):
	__tablename__ = 'userAnswer'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_id = db.Column(db.Integer, ForeignKey('questionChoice.id'))

# this is an attempt of a quiz. The date and data scoresheet has been recorded	
#class Result(db.Model):
#	id = db.Column(db.Integer, primary_key=True)
#	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#	
#	flagQuiz = db.Column(db.Boolean, default=False)
#	worldQuiz = db.Column(db.Boolean, default=False)
#	score = db.Column(db.Integer)
#	date_of_attempt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# create sample users
#db.drop_all()
db.create_all()

"""
user_1 = User(username="JohnDoe", email="John@hotmail.com", admin=False, password_hash="notASecret")

user_2 = User(username="Nick", email="nick@gmail.com", admin=True, password_hash="blahblah")


db.session.add(user_1)
db.session.add(user_2)
"""

users = User.query.all()
print("Array of Users Registered: ")
print(users)

db.session.commit()

