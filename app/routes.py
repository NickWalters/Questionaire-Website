from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from decimal import Decimal



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		if User.is_admin(current_user):
			return redirect(url_for('hoster'))
		else:
			return redirect(url_for('index'))
	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if User.is_admin(current_user):
			return redirect(url_for('hoster'))
		if not next_page or url_parse(next_page).netloc !='':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have Logged Out")
	return redirect(url_for('prelogin'))
	
@app.route('/index')
def index():
	if current_user.is_authenticated:
		if current_user.admin == False:
			return render_template('index.html')
		else:
			flash("You are an Admin")
			return render_template('index.html')
	else:
		return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	#if current_user.is_authenticated:
	#	return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	
	return render_template('register.html', title='Register', form=form)
	

@app.route('/prelogin')
@app.route('/')
def prelogin():
	if current_user.is_authenticated:
		return render_template('index.html')
	return render_template('prelogin.html')

@app.route('/')
def home():
 	return render_template('index.html')

@app.route('/quizSelect')
@login_required
def quizSelect():
	return render_template('quizSelect.html', quizzes = Quiz.query.all())

@app.route('/quiz/<string:quiz_name>', methods=['GET', 'POST'])
def quiz(quiz_name):
	print(quiz_name)
	quiz = None
	for quiz in Quiz.query.all():
		if quiz_name == quiz.short(): break
	quizStyle = quiz.quizStyle

	if session.get('question_number') != None:
		question_number = session.pop('question_number', None)
		question = quiz.get_question_by_question_number(question_number)
		form = make_form(quizStyle, question)
		submitted_form = request.form
		if submitted_form:
			submitted_choice = None
			print(quizStyle)
			if quizStyle.id == 1 :
				choices = db.session.query(QuestionChoice).all()
				submitted_choice = submitted_form.get('radioField')
			elif quizStyle.id == 2:
				choices = db.session.query(QuestionChoice).all()
				i = 0
				choices_array = question.get_question_choices_as_array_of_pairs()
				print(choices_array[i][1])
				
				what = list(submitted_form.values())[0]

				for choice in choices:
					if choice.question_id == question.id and choice.choice_content == what:
						thing = choice.choice_number
						print(thing)
						submitted_choice = thing

				print('below is wtf')
				print(what)
				'''while i < form.len:
					choices_array = question.get_question_choices_as_array_of_pairs()
					if choices_array[i][1] == list(submitted_form.values())[0]:
						submitted_choice = i
						print('sub inside loop')
						print(choices_array[i][1])
						break
					i = i + 1
			print('below is submitted chocie')
			print(submitted_choice)'''
			answer = UserAnswer(user_id=current_user.id,question_id=question.id,choice_id=submitted_choice)
			db.session.add(answer)
			db.session.commit()
			next_question = quiz.get_next_question(last_question = question)
			if next_question != None:
				session['question_number']=next_question.question_number
				next_form = make_form(quizStyle, next_question)
				return render_template(quizStyle.template_file,quiz = quiz,question = next_question,form = next_form)
			score = 0
			answers = db.session.query(UserAnswer).all()
			
			print('before for loop')

			print(answers)
			if quiz_name == 'lang':
				for answer in answers:
					for choice in choices:
						if choice.question_id == answer.question_id and answer.choice_id == choice.choice_number and choice.choice_correct == True and answer.user_id == current_user.id:
							score = score + 1
							print('new for loop')
			
			if quiz_name =='flag':
				for answer in answers:
					for choice in choices:
						if choice.id == answer.choice_id and choice.choice_correct == True and answer.user_id == current_user.id:
							print('im inside hehe')
							score = score + 1
						
				
			db.session.query(UserAnswer).delete()
			db.session.commit()
			prevscoretext = ''
			averagescore = 0
			improvetext = ''
			attemptnumber = 0
			if quiz_name == "lang":
				print('this is the language quiz baby')
				prevscoretext = 'this is the lang'
				averagescore = 100
				improvetext = 'yoyoyo'
				attemptnumber = 9 
			if quiz_name == 'flag':
				attempts = db.session.query(User_attempt)
				count = attempts.count()
				prevscore = 0
				averagescore = 0
				attemptnumber = 0
				here = 0
				print('count is:' + str(count))
				if count == 0:
					db.session.add(User_attempt(totalscore = score, attemptnum = 1, prevattempt = score, user_id = current_user.id, quiz_id = 1))
					averagescore = score
					attemptnum = 1
					db.session.commit()
					print('why here')
				else:
					print('else statement')
					for attempt in attempts:
						if attempt.user_id == current_user.id:
							here = 1
				if here == 1:
					update = User_attempt.query.filter_by(user_id = current_user.id).first()
					update.totalscore = update.totalscore + score
					update.attemptnum = update.attemptnum + 1
					prevscore = update.prevattempt
					update.prevattempt = score
					averagescore = round((Decimal(update.totalscore / update.attemptnum)),2)
					attemptnumber = update.attemptnum
					print('average score is: ' + str(averagescore))
					db.session.commit()
					print("if ")
					print('prev score = ' +  str(prevscore))
				elif here == 0:
					db.session.add(User_attempt(totalscore = score, attemptnum = 1, prevattempt = score, user_id = current_user.id))
					averagescore = score
					attemptnumber = 1
					db.session.commit()
					print("elseaddign")
				print("after")
				print(prevscore)
				prevscoretext = ''
				improvetext = ''
				if prevscore == 0:
					prevscoretext = 'Last attempt: You havent attempted the quiz before.' 
				else:
					prevscoretext = 'Your previous attempt score was: ' + str(prevscore)
					if score > prevscore:
						improvetext = 'You have improved by' + str(score - prevscore) + '0%'
					elif score < prevscore:
						improvetext = 'Somehow your score went down by ' + str(score - prevscore) + '0% what happened?!'
					elif score == 10 and prevscore ==10:
						improvetext = 'Great job!'
					elif score == prevscore:
						improvetext = 'No improvement, keep trying!'	
						
			return render_template('results.html',quiz = quiz, score = score, prevscoretext = prevscoretext, averagescore = averagescore, improvetext =improvetext, attemptnumber = attemptnumber )
		#if no form submitted
		else :
			return render_template(quizStyle.template_file,quiz = quiz,question = question,form = form)
	#If starting from the beginning, no cookie
	question=quiz.get_first_question()
	session['question_number'] = question.question_number
	form = make_form(quizStyle, question)
	return render_template(quizStyle.template_file,quiz = quiz,question = question,form = form)

def make_form(style, question):
	if style.id == 1:
		return StyleOneForm(question.get_question_choices_as_array_of_pairs())
	else :#style.id == 2:
		return StyleTwoForm(question.get_question_choices_as_array_of_pairs())

@app.route('/languageQuiz')
def languageQuiz():
	return render_template('HTML-languageQuizFinal.html')

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quiz, db.session))
admin.add_view(ModelView(QuizStyle, db.session))
admin.add_view(ModelView(QuizContent, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(QuestionChoice, db.session))
admin.add_view(ModelView(QuestionContent, db.session))
admin.add_view(ModelView(UserAnswer, db.session))

@app.route('/hoster')
@login_required
def hoster():

	if current_user.admin == True: 
		users = User.query.all()

		quiz = db.session.query(Quiz)
		# quiz = db.session.query(Quiz).join(Question)

		return render_template('admin.html', users=users, quiz=quiz)
	
	else:
		flash('Cannot access admin page directly')
		return redirect(url_for('index'))


@app.route('/results')
@login_required
def results():
	score = 0
	answers = db.session.query(UserAnswer)
	choices = db.session.query(QuestionChoice)
	for answers1 in answers:
		for choices1 in choices:
			if choices1.id == answers1.choice_id and choices1.choice_correct == True and answers1.user_id == current_user.id:
				score = score + 1

	return render_template('results.html', score = score)
