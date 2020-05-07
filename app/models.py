from app import db, login
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_migrate import Migrate

#Drop all tables from the DB
#db.drop_all()
#db.session.commit()

class User(UserMixin, db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	admin = db.Column(db.Boolean, default=False, nullable=False) 
	password_hash = db.Column(db.String(128))

	userAnswers = db.relationship('UserAnswer', backref='user', lazy="dynamic")
	quizzes = db.relationship('Quiz', back_populates="creator")
	
	def is_admin(self):
		return self.admin

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return 'User: {}'.format(self.username)+' (admin:{}'.format(self.admin)+')'

class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer,primary_key=True)
	quizname = db.Column(db.String(80), index=True)

	creator_id = db.Column(db.Integer, ForeignKey('user.id'))
	creator = relationship('User', back_populates="quizzes")

	style = db.Column(db.Integer, ForeignKey('quizStyle.id'))
	quizStyle = relationship('QuizStyle', back_populates="quizzes")

	questions = db.relationship('Question', backref='quiz', lazy=True)

	def __repr__(self):
		return '<Quiz {}>'.format(self.quizname)


class QuizStyle(db.Model):
	__tablename__ = 'quizStyle'
	id = db.Column(db.Integer,primary_key=True)
	style_name = db.Column(db.String(64), index=True, unique=True)
	template_file = db.Column(db.String(64))

	quizzes = db.relationship('Quiz', back_populates="quizStyle")

	#styleJs = db.relationship('StyleJs', backref='style', lazy=True)
	#styleCss = db.relationship('StyleCss', backref='style', lazy=True)

	def __repr__(self):
		return '<Style: {}>'.format(self.style_name)

"""
class StyleJs(db.Model):
	__tablename__ = 'styleJs'
	id = db.Column(db.Integer, ForeignKey('quizStyle.id'))
	content = db.Column(db.String(80))

	def __repr__(self):
		return '<QuizJs {}>'.format(self.content)

class StyleCss(db.Model):
	__tablename__ = 'styleCss'
	id = db.Column(db.Integer, ForeignKey('quizStyle.id'))
	content = db.Column(db.String(80))

	def __repr__(self):
		return '<QuizCss {}>'.format(self.content)
"""

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer,primary_key=True)
	quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'))
	question_number = db.Column(db.Integer)

	question_choices = db.relationship('QuestionChoice', backref='question', lazy='dynamic')
	question_contents = db.relationship('QuestionContent', backref='question', lazy='dynamic')
	question_answers = db.relationship('UserAnswer', backref='question', lazy=True)

	def __repr__(self):
		return '<Quiz {}'.format(self.quiz_id)+':Q{}>'.format(self.question_number)

class QuestionContent(db.Model):
	__tablename__ = 'questionContent'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	text_content = db.Column(db.String(80))
	img_content = db.Column(db.String(80))
	
	def __repr__(self):
		return '<Question {}>'.format(self.question_id)

class QuestionChoice(db.Model):
	__tablename__ = 'questionChoice'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_number = db.Column(db.Integer)
	choice_content = db.Column(db.String(80))
	choice_correct = db.Column(db.Boolean)
	
	#choice_chosen = db.relationship('UserAnswer', backref='questionChoice', lazy=True)
	
	def __repr__(self):
		return '<Choice {}>'.format(self.choice_content)

class UserAnswer(db.Model):
	__tablename__ = 'userAnswer'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_id = db.Column(db.Integer, ForeignKey('questionChoice.id'))
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)

	def __repr__(self):
		return '<Answers {}>'.format(self.id)
		
@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#Create DB models
db.create_all()



#Print all DB data
print(User.query.all())
print(Quiz.query.all())
print(QuizStyle.query.all())
print(Question.query.all())
print(QuestionContent.query.all())
#print(QuestionChoice.query.all())
print(UserAnswer.query.all())