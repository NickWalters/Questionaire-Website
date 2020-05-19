from app import db, login
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, desc
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_migrate import Migrate

class User(UserMixin, db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	admin = db.Column(db.Boolean, default=False, nullable=False) 
	password_hash = db.Column(db.String(128))

	userAnswers = db.relationship('UserAnswer', backref='user', lazy="dynamic")
	quizzes = db.relationship('Quiz', back_populates="creator")
	attempt = db.relationship('User_attempt', backref='author', lazy=True)
	
	def is_admin(self):
		return self.admin

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_last_answer(self, quiz):
		lastanswer = None
		for question in quiz.questions:
			for answer in question.user_answers:
				if answer.user_id==current_user.id:
					if lastanswer == None:
						lastanswer=answer
					elif lastanswer.id<answer.id:
						lastanswer = answer
		#quiz.questions.user_answers.filter_by(user_id=id).order_by(UserAnswer.timestamp).first()
		return lastanswer

	def __repr__(self):
		return 'User: {}'.format(self.username)+' (admin:{}'.format(self.admin)+')'
		
class User_attempt(db.Model):
	__tablename__ ='userattempt'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
	totalscore = db.Column(db.Integer)
	attemptnum = db.Column(db.Integer)
	prevattempt = db.Column(db.Integer)
	def __repr__(self):
		return '<id:{}'.format(self.id)+' user_id:{}'.format(self.user_id)+ 'total:{}'.format(self.totalscore) + 'attemptnum:{}'.format(self.attemptnum) +'quiz id:{}'.format(self.quiz_id)



class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer,primary_key=True)
	quizname = db.Column(db.String(80), index=True)

	creator_id = db.Column(db.Integer, ForeignKey('user.id'))
	creator = relationship('User', back_populates="quizzes")

	style = db.Column(db.Integer, ForeignKey('quizStyle.id'))
	quizStyle = relationship('QuizStyle', back_populates="quizzes")
	questions = db.relationship('Question', backref='quiz', lazy='dynamic')
	quizContents = db.relationship('QuizContent', backref='quiz', lazy='dynamic')
	
	def short(self):
		return self.quizname.split(' ', 1)[0].lower()

	def get_first_question(self):
		return self.questions.filter_by(question_number=1).first()

	def get_next_question(self, last_question):
		return self.questions.filter_by(question_number=last_question.question_number+1).first()

	def get_question_by_question_number(self, question_number):
		return self.questions.filter_by(question_number = question_number).first()

	def __repr__(self):
		return '<id:{}'.format(self.id) +'<quiz name:{}'.format(self.quizname) 

class QuizContent(db.Model):
	__tablename__ = 'quizContent'
	id = db.Column(db.Integer,primary_key=True)
	quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'))
	text_content = db.Column(db.String(128))
	img_content = db.Column(db.String(80))
	
	def __repr__(self):
		return str(self.id)

class QuizStyle(db.Model):
	__tablename__ = 'quizStyle'
	id = db.Column(db.Integer,primary_key=True)
	style_name = db.Column(db.String(64), index=True, unique=True)
	template_file = db.Column(db.String(64))

	quizzes = db.relationship('Quiz', back_populates="quizStyle")

	#styleJs = db.relationship('StyleJs', backref='style', lazy=True)
	#styleCss = db.relationship('StyleCss', backref='style', lazy=True)

	def __repr__(self):
		return self.style_name

class Question(db.Model):
	__tablename__ = 'question'
	id = db.Column(db.Integer,primary_key=True)
	quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'))
	question_number = db.Column(db.Integer)

	question_choices = db.relationship('QuestionChoice', backref='question', lazy='dynamic')
	question_contents = db.relationship('QuestionContent', backref='question', lazy='dynamic')
	
	user_answers = db.relationship('UserAnswer', back_populates="answered_question")

	def get_question_choices_as_array_of_pairs(self):
		choices = []
		for choice in self.question_choices:
			choices.append((choice.choice_number,choice.choice_content))
		return choices
	
	def __repr__(self):
		return '< id:{}'.format(self.id)+' quiz_id:{}'.format(self.quiz_id) +' question num:{}'.format(self.question_number)
class QuestionContent(db.Model):
	__tablename__ = 'questionContent'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	text_content = db.Column(db.String(80))
	img_content = db.Column(db.String(80))
	
	def __repr__(self):
		return str(self.id)

class QuestionChoice(db.Model):
	__tablename__ = 'questionChoice'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_number = db.Column(db.Integer)
	choice_content = db.Column(db.String(80))
	choice_correct = db.Column(db.Boolean)
	
	#choice_chosen = db.relationship('UserAnswer', backref='questionChoice', lazy=True)
	
	def __repr__(self):
		return ' id:{}'.format(self.id) +'<question_id:{}'.format(self.question_id) +'<choice num:{}'.format(self.choice_number) + '< correct :{}'.format(self.choice_correct) + '<choice content:{}'.format(self.choice_content)  

class UserAnswer(db.Model):
	__tablename__ = 'userAnswer'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_id = db.Column(db.Integer, ForeignKey('questionChoice.id'))
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)
	
	answered_question = db.relationship('Question', back_populates="user_answers")
	def __repr__(self):
		return '<Answer id:{}'.format(self.id)+' user_id:{}'.format(self.user_id)+' question_id:{}'.format(self.question_id)+' choice_id_id:{}'.format(self.choice_id)+'>'

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#Create DB models
db.create_all()
#db.drop_all()
#db.session.query(UserAnswer).delete()
#db.session.query(User_attempt).delete()
#db.session.add(User_attempt(totalscore = 1, attemptnum = 1, prevattempt = 1, user_id = 1, quiz_id = 1))
#db.session.commit()


#Print all DB data
print(User_attempt.query.all())

#Print all DB data
#print(User.query.all())

print(Quiz.query.all())
#print(QuizStyle.query.all())
#print(Question.query.all())
#print(QuestionContent.query.all())
#print(QuestionChoice.query.all())
#print(UserAnswer.query.all())
