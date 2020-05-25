from app import db, login, admin
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, desc
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

class User(UserMixin, db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True, nullable=False)
	email = db.Column(db.String(120), index=True, unique=True, nullable=False)
	admin = db.Column(db.Boolean, default=False, nullable=False) 
	password_hash = db.Column(db.String(128), nullable=False)

	userAttempts = db.relationship('UserAttempt', backref='user', lazy='dynamic')
	quizzes = db.relationship('Quiz', back_populates='creator')
	
	def is_admin(self):
		return self.admin

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_user_quiz_attempts(self, quiz):
		return self.userAttempts.filter_by(quiz_id = quiz.id)

	def get_last_attempt(self, userAttempts):
		lastAttempt = None
		for attempt in userAttempts:
			if lastAttempt == None:
				lastAttempt = attempt
			elif lastAttempt.id<attempt.id:
				lastAttempt = attempt
		#quiz.questions.user_answers.filter_by(user_id=id).order_by(UserAnswer.timestamp).first()
		return lastAttempt

	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return 'User: {}'.format(self.username)+' (admin:{}'.format(self.admin)+')'

class Quiz(db.Model):
	__tablename__ = 'quiz'
	id = db.Column(db.Integer,primary_key=True)
	quizname = db.Column(db.String(80), index=True)

	creator_id = db.Column(db.Integer, ForeignKey('user.id'))
	creator = relationship('User', back_populates="quizzes")

	style = db.Column(db.Integer, ForeignKey('quizStyle.id'))
	quizStyle = relationship('QuizStyle', back_populates="quizzes")
	questions = db.relationship('Question', back_populates='quiz', lazy='dynamic')
	quizContents = db.relationship('QuizContent', backref='quiz', lazy='dynamic')
	attempts = db.relationship('UserAttempt', backref='quiz', lazy='dynamic')

	def short(self):
		return self.quizname.split(' ', 1)[0].lower()

	def get_first_question(self):
		return self.questions.filter_by(question_number=1).first()

	def get_next_question(self, last_question):
		return self.questions.filter_by(question_number=last_question.question_number+1).first()

	def get_question_by_question_number(self, question_number):
		return self.questions.filter_by(question_number = question_number).first()
	
	def get_average_score(self, user):
		total_score = 0
		if user:
			user_attempts = self.attempts.filter_by(user_id = user.id)
			for attempt in user_attempts:
				total_score = total_score + attempt.get_score()
			if user_attempts.count() == 0: return None
			return round(total_score/user_attempts.count(),2)
		else:
			for attempt in self.attempts:
				total_score = total_score + attempt.get_score()
			if self.attempts.count() == 0: return None
			return round(total_score/self.attempts.count(),2)

	def __repr__(self):
		return self.quizname

	def as_str(self):
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


	userAnswers = db.relationship('UserAnswer', back_populates='question')
	quiz = db.relationship('Quiz', back_populates='questions')

	def get_question_choices_as_array_of_pairs(self):
		choices = []
		for choice in self.question_choices:
			choices.append((choice.choice_number,choice.choice_content))
		return choices
	
	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return '< id:{}'.format(self.id)+' quiz_id:{}'.format(self.quiz_id) +' question num:{}'.format(self.question_number)

class QuestionContent(db.Model):
	__tablename__ = 'questionContent'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	text_content = db.Column(db.String(80))
	img_content = db.Column(db.String(80))
	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return str(self.id)

class QuestionChoice(db.Model):
	__tablename__ = 'questionChoice'
	id = db.Column(db.Integer,primary_key=True)
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_number = db.Column(db.Integer)
	choice_content = db.Column(db.String(80))
	choice_correct = db.Column(db.Boolean)
	userAnswers = db.relation('UserAnswer', back_populates='questionChoice')
	#choice_chosen = db.relationship('UserAnswer', backref='questionChoice', lazy=True)
	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return ' id:{}'.format(self.id) +'<question_id:{}'.format(self.question_id) +'<choice num:{}'.format(self.choice_number) + '< correct :{}'.format(self.choice_correct) + '<choice content:{}'.format(self.choice_content)
		
class UserAttempt(db.Model):
	__tablename__ ='userAttempt'
	id = db.Column(db.Integer, primary_key=True)
	attempt_number = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
	#totalscore = db.Column(db.Integer)
	#attemptnum = db.Column(db.Integer)
	#prevattempt = db.Column(db.Integer)

	userAnswers = db.relation('UserAnswer', backref='userAttempt', lazy='dynamic')

	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return '<id:{}'.format(self.id)+' user_id:{}'.format(self.user_id)+ 'total:{}'.format(self.totalscore) + 'attemptnum:{}'.format(self.attemptnum) +'quiz id:{}'.format(self.quiz_id)

	def get_score(self):
		score = 0
		for answer in self.userAnswers:
			if answer.questionChoice.choice_correct: score = score + 1
		return score

class UserAnswer(db.Model):
	__tablename__ = 'userAnswer'
	id = db.Column(db.Integer, primary_key=True)
	attempt_id = db.Column(db.Integer, ForeignKey('userAttempt.id'))
	user_id = db.Column(db.Integer, ForeignKey('user.id'))
	question_id = db.Column(db.Integer, ForeignKey('question.id'))
	choice_id = db.Column(db.Integer, ForeignKey('questionChoice.id'))
	timestamp = db.Column(db.DateTime, default = datetime.utcnow)
	
	questionChoice = db.relation('QuestionChoice', back_populates='userAnswers')
	question = db.relationship('Question', back_populates='userAnswers')

	def __repr__(self):
		return str(self.id)

	def as_str(self):
		return '<Answer id:{}'.format(self.id)+' user_id:{}'.format(self.user_id)+' question_id:{}'.format(self.question_id)+' choice_id_id:{}'.format(self.choice_id)+'>'

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quiz, db.session))
admin.add_view(ModelView(QuizStyle, db.session))
admin.add_view(ModelView(QuizContent, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(QuestionChoice, db.session))
admin.add_view(ModelView(QuestionContent, db.session))
admin.add_view(ModelView(UserAnswer, db.session))
admin.add_view(ModelView(UserAttempt, db.session))

#Create DB models
db.create_all()

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


''''
db.session.add(User(username="admin", email="admin@admin.admin", admin=True, password_hash=generate_password_hash("admin")))
db.session.add(User(username="user", email="user@user.user", admin=False, password_hash=generate_password_hash("user")))

db.session.add(Quiz(quizname="Flag Quiz",creator_id=1,style=1))

db.session.add(QuizStyle(style_name="Old flag style",template_file="quizStyle1.html"))

db.session.add(QuizContent(quiz_id=1,text_content="Are you truly aware of the outside world? Do you have what it takes to test your knowledge on the flags of the world? Take our test !",img_content="au.svg"))

db.session.add(Question(quiz_id=1,question_number=1))
db.session.add(Question(quiz_id=1,question_number=2))
db.session.add(Question(quiz_id=1,question_number=3))
db.session.add(Question(quiz_id=1,question_number=4))
db.session.add(Question(quiz_id=1,question_number=5))
db.session.add(Question(quiz_id=1,question_number=6))
db.session.add(Question(quiz_id=1,question_number=7))
db.session.add(Question(quiz_id=1,question_number=8))
db.session.add(Question(quiz_id=1,question_number=9))
db.session.add(Question(quiz_id=1,question_number=10))

db.session.add(QuestionContent(question_id=1,text_content="What country flag is this?",img_content="flag01.svg"))
db.session.add(QuestionContent(question_id=2,text_content="What country flag is this?",img_content="flag02.svg"))
db.session.add(QuestionContent(question_id=3,text_content="What country flag is this?",img_content="flag03.svg"))
db.session.add(QuestionContent(question_id=4,text_content="What country flag is this?",img_content="flag04.svg"))
db.session.add(QuestionContent(question_id=5,text_content="What country flag is this?",img_content="flag05.svg"))
db.session.add(QuestionContent(question_id=6,text_content="What country flag is this?",img_content="flag06.svg"))
db.session.add(QuestionContent(question_id=7,text_content="What country flag is this?",img_content="flag07.svg"))
db.session.add(QuestionContent(question_id=8,text_content="What country flag is this?",img_content="flag08.svg"))
db.session.add(QuestionContent(question_id=9,text_content="What country flag is this?",img_content="flag09.svg"))
db.session.add(QuestionContent(question_id=10,text_content="What country flag is this?",img_content="flag10.svg"))

#Question choices for flag quiz
db.session.add(QuestionChoice(question_id=1,choice_number=1,choice_content="Namibia",choice_correct=False))
db.session.add(QuestionChoice(question_id=1,choice_number=2,choice_content="Turks and Caicos Islands",choice_correct=False))
db.session.add(QuestionChoice(question_id=1,choice_number=3,choice_content="Mongolia",choice_correct=False))
db.session.add(QuestionChoice(question_id=1,choice_number=4,choice_content="Saint Pierre and Miquelon",choice_correct=True))

db.session.add(QuestionChoice(question_id=2,choice_number=1,choice_content="French Polynesia",choice_correct=False))
db.session.add(QuestionChoice(question_id=2,choice_number=2,choice_content="Maldives",choice_correct=False))
db.session.add(QuestionChoice(question_id=2,choice_number=3,choice_content="Djibouti",choice_correct=False))
db.session.add(QuestionChoice(question_id=2,choice_number=4,choice_content="Botswana",choice_correct=True))

db.session.add(QuestionChoice(question_id=3,choice_number=1,choice_content="Anguilla",choice_correct=False))
db.session.add(QuestionChoice(question_id=3,choice_number=2,choice_content="Lesotho",choice_correct=False))
db.session.add(QuestionChoice(question_id=3,choice_number=3,choice_content="Western Sahara",choice_correct=False))
db.session.add(QuestionChoice(question_id=3,choice_number=4,choice_content="Gabon",choice_correct=True))

db.session.add(QuestionChoice(question_id=4,choice_number=1,choice_content="Heard Island and McDonald Islands",choice_correct=False))
db.session.add(QuestionChoice(question_id=4,choice_number=2,choice_content="American Samoa",choice_correct=False))
db.session.add(QuestionChoice(question_id=4,choice_number=3,choice_content="Zimbabwe",choice_correct=False))
db.session.add(QuestionChoice(question_id=4,choice_number=4,choice_content="Puerto Rico",choice_correct=True))

db.session.add(QuestionChoice(question_id=5,choice_number=1,choice_content="Isle of Man",choice_correct=False))
db.session.add(QuestionChoice(question_id=5,choice_number=2,choice_content="South Georgia and the South Sandwich Islands",choice_correct=False))
db.session.add(QuestionChoice(question_id=5,choice_number=3,choice_content="Iran",choice_correct=False))
db.session.add(QuestionChoice(question_id=5,choice_number=4,choice_content="Pitcairn",choice_correct=True))

db.session.add(QuestionChoice(question_id=6,choice_number=1,choice_content="Korea (Republic of)",choice_correct=False))
db.session.add(QuestionChoice(question_id=6,choice_number=2,choice_content="Cayman Islands",choice_correct=False))
db.session.add(QuestionChoice(question_id=6,choice_number=3,choice_content="Myanmar",choice_correct=False))
db.session.add(QuestionChoice(question_id=6,choice_number=4,choice_content="Kiribati",choice_correct=True))

db.session.add(QuestionChoice(question_id=7,choice_number=1,choice_content="Slovenia",choice_correct=False))
db.session.add(QuestionChoice(question_id=7,choice_number=2,choice_content="Brunei",choice_correct=False))
db.session.add(QuestionChoice(question_id=7,choice_number=3,choice_content="Saint Martin (French part)",choice_correct=False))
db.session.add(QuestionChoice(question_id=7,choice_number=4,choice_content="Suriname",choice_correct=True))

db.session.add(QuestionChoice(question_id=8,choice_number=1,choice_content="Finland",choice_correct=False))
db.session.add(QuestionChoice(question_id=8,choice_number=2,choice_content="Fiji",choice_correct=False))
db.session.add(QuestionChoice(question_id=8,choice_number=3,choice_content="Bahamas",choice_correct=False))
db.session.add(QuestionChoice(question_id=8,choice_number=4,choice_content="Colombia",choice_correct=True))

db.session.add(QuestionChoice(question_id=9,choice_number=1,choice_content="Rwanda",choice_correct=False))
db.session.add(QuestionChoice(question_id=9,choice_number=2,choice_content="Georgia",choice_correct=False))
db.session.add(QuestionChoice(question_id=9,choice_number=3,choice_content="Palestine",choice_correct=False))
db.session.add(QuestionChoice(question_id=9,choice_number=4,choice_content="Czechia",choice_correct=True))

db.session.add(QuestionChoice(question_id=10,choice_number=1,choice_content="Afghanistan",choice_correct=False))
db.session.add(QuestionChoice(question_id=10,choice_number=2,choice_content="Indonesia",choice_correct=False))
db.session.add(QuestionChoice(question_id=10,choice_number=3,choice_content="Angola",choice_correct=False))
db.session.add(QuestionChoice(question_id=10,choice_number=4,choice_content="Jersey",choice_correct=True))

db.session.add(Quiz(quizname="Language Quiz",creator_id=1,style=2))

db.session.add(QuizStyle(style_name="Language quiz style",template_file="quizStyle2.html"))

db.session.add(QuizContent(quiz_id=2,text_content="How much do you know about world culture, information and languages?",img_content="people-banner.png"))

db.session.add(Question(quiz_id=2,question_number=1))
db.session.add(Question(quiz_id=2,question_number=2))
db.session.add(Question(quiz_id=2,question_number=3))
db.session.add(Question(quiz_id=2,question_number=4))
db.session.add(Question(quiz_id=2,question_number=5))
db.session.add(Question(quiz_id=2,question_number=6))
db.session.add(Question(quiz_id=2,question_number=7))
db.session.add(Question(quiz_id=2,question_number=8))
db.session.add(Question(quiz_id=2,question_number=9))
db.session.add(Question(quiz_id=2,question_number=10))

db.session.add(QuestionContent(question_id=11,text_content="What is the Official Language of Taiwan",img_content="taiwan-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=12,text_content="What is the Official Language of Australia",img_content="australia-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=13,text_content="What is the Official Language of Norway",img_content="norway-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=14,text_content="What is the Official Language of Colombia",img_content="colombia-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=15,text_content="What is the Official Language of Pakistan",img_content="pakistan-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=16,text_content="What is the Official Language of Ukraine",img_content="ukraine-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=17,text_content="What is the Official Language of Malaysia",img_content="malaysia-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=18,text_content="What is the Official Language of Mexico",img_content="mexico-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=19,text_content="What is the Official Language of Iran",img_content="iran-languageQuiz.jpg"))
db.session.add(QuestionContent(question_id=20,text_content="What is the Official Language of Indonesia",img_content="indonesia-languageQuiz.jpg"))

db.session.add(QuestionChoice(question_id=11,choice_number=1,choice_content="Taiwanese",choice_correct=False))
db.session.add(QuestionChoice(question_id=11,choice_number=2,choice_content="Japanese",choice_correct=False))
db.session.add(QuestionChoice(question_id=11,choice_number=3,choice_content="Mandarin",choice_correct=True))
db.session.add(QuestionChoice(question_id=11,choice_number=4,choice_content="Cantonese",choice_correct=False))

db.session.add(QuestionChoice(question_id=12,choice_number=1,choice_content="English",choice_correct=True))
db.session.add(QuestionChoice(question_id=12,choice_number=2,choice_content="German",choice_correct=False))
db.session.add(QuestionChoice(question_id=12,choice_number=3,choice_content="Korean",choice_correct=False))
db.session.add(QuestionChoice(question_id=12,choice_number=4,choice_content="Russian",choice_correct=False))

db.session.add(QuestionChoice(question_id=13,choice_number=1,choice_content="German",choice_correct=False))
db.session.add(QuestionChoice(question_id=13,choice_number=2,choice_content="Spanish",choice_correct=False))
db.session.add(QuestionChoice(question_id=13,choice_number=3,choice_content="English",choice_correct=False))
db.session.add(QuestionChoice(question_id=13,choice_number=4,choice_content="Romani",choice_correct=True))

db.session.add(QuestionChoice(question_id=14,choice_number=1,choice_content="Spanish",choice_correct=True))
db.session.add(QuestionChoice(question_id=14,choice_number=2,choice_content="Irish",choice_correct=False))
db.session.add(QuestionChoice(question_id=14,choice_number=3,choice_content="Dutch",choice_correct=False))
db.session.add(QuestionChoice(question_id=14,choice_number=4,choice_content="French",choice_correct=False))

db.session.add(QuestionChoice(question_id=15,choice_number=1,choice_content="Perish",choice_correct=False))
db.session.add(QuestionChoice(question_id=15,choice_number=2,choice_content="Hindi",choice_correct=False))
db.session.add(QuestionChoice(question_id=15,choice_number=3,choice_content="Arabic",choice_correct=False))
db.session.add(QuestionChoice(question_id=15,choice_number=4,choice_content="Urdu",choice_correct=True))

db.session.add(QuestionChoice(question_id=16,choice_number=1,choice_content="Ukrainian",choice_correct=True))
db.session.add(QuestionChoice(question_id=16,choice_number=2,choice_content="Russian",choice_correct=False))
db.session.add(QuestionChoice(question_id=16,choice_number=3,choice_content="Greenlandic",choice_correct=False))
db.session.add(QuestionChoice(question_id=16,choice_number=4,choice_content="Galician",choice_correct=False))

db.session.add(QuestionChoice(question_id=17,choice_number=1,choice_content="Malaysian",choice_correct=False))
db.session.add(QuestionChoice(question_id=17,choice_number=2,choice_content="Malayense",choice_correct=False))
db.session.add(QuestionChoice(question_id=17,choice_number=3,choice_content="Mandarin",choice_correct=False))
db.session.add(QuestionChoice(question_id=17,choice_number=4,choice_content="Malay",choice_correct=True))

db.session.add(QuestionChoice(question_id=18,choice_number=1,choice_content="Spanish",choice_correct=True))
db.session.add(QuestionChoice(question_id=18,choice_number=2,choice_content="Mexian",choice_correct=False))
db.session.add(QuestionChoice(question_id=18,choice_number=3,choice_content="Portuguese",choice_correct=False))
db.session.add(QuestionChoice(question_id=18,choice_number=4,choice_content="Welsh",choice_correct=False))

db.session.add(QuestionChoice(question_id=19,choice_number=1,choice_content="Arabic",choice_correct=False))
db.session.add(QuestionChoice(question_id=19,choice_number=2,choice_content="Hebrew",choice_correct=False))
db.session.add(QuestionChoice(question_id=19,choice_number=3,choice_content="Persian",choice_correct=True))
db.session.add(QuestionChoice(question_id=19,choice_number=4,choice_content="Hindi",choice_correct=False))

db.session.add(QuestionChoice(question_id=20,choice_number=1,choice_content="Malay",choice_correct=False))
db.session.add(QuestionChoice(question_id=20,choice_number=2,choice_content="Indonesia",choice_correct=True))
db.session.add(QuestionChoice(question_id=20,choice_number=3,choice_content="Mandarin",choice_correct=False))
db.session.add(QuestionChoice(question_id=20,choice_number=4,choice_content="Thai",choice_correct=False))
db.session.commit()'''