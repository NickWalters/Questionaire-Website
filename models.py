from app import db
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_migrate import Migrate

#db.drop_all()

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
		return 'User: {}'.format(self.username)+' (admin:{}'.format(self.admin)+')'

class Style(db.Model):
	__tablename__ = 'style'
	id = db.Column(db.Integer,primary_key=True)

class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer,primary_key=True)
	quizname = db.Column(db.String(80))
	creator_id = db.Column(db.Integer, ForeignKey('user.id'))
	style = db.Column(db.Integer, ForeignKey('style.id'))
	quiz_content = db.Column(db.String(80))
	#questions = db.relationship('Question', backref='person', lazy=True)

	def __repr__(self):
		return '<Quiz {}>'.format(self.quizname)

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer,primary_key=True)
	quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'))
	question_number = db.Column(db.Integer)
	question_content = db.Column(db.String(80))
	#question_choices = db.relationship('QuestionChoice', backref='person', lazy=True)
	def __repr__(self):
		return '<Question {}>'.format(self.question_content)

class QuestionChoice(db.Model):
	__tablename__ = 'questionChoice'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_number = db.Column(db.Integer)
	choice_content = db.Column(db.String(80))
	choice_correct = db.Column(db.Boolean)
	#choice_chosen = db.relationship('UserAnswer', backref='person', lazy=True)
	
	def __repr__(self):
		return '<Choice {}>'.format(self.choice_content)

class UserAnswer(db.Model):
	__tablename__ = 'userAnswer'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_id = db.Column(db.Integer, ForeignKey('questionChoice.id'))

	def __repr__(self):
		return '<Answers {}>'.format(self.id)

db.create_all()

#db.session.query(User).delete()
#db.session.query(Quiz).delete()
#db.session.query(Question).delete()
#db.session.query(QuestionChoice).delete()
#db.session.query(UserAnswer).delete()

#db.session.add(User(username="Admin", email="admin@admin.admin", admin=True, password_hash="password"))
#db.session.add(User(username="User", email="user@user.user", admin=False, password_hash="password"))
#db.session.add(Quiz(quizname="Flag Quiz"))
#db.session.add(Question(quiz_id=1,question_number=1,question_content="1"))
#db.session.add(QuestionChoice(question_id=1,choice_number=1,choice_content="1",choice_correct=True))
#db.session.add(UserAnswer(user_id=1,question_id=1,choice_id=1))

#db.session.commit()

print(User.query.all())
print(Quiz.query.all())
print(Question.query.all())
print(QuestionChoice.query.all())
print(UserAnswer.query.all())