from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from decimal import Decimal

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
	
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc !='':
			next_page = url_for('home')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have Logged Out")
	return redirect(url_for('home'))
	
@app.route('/')
def home():
	if current_user.is_authenticated:
		if current_user.admin:
			flash("You are an Admin")
			return render_template('index.html')
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

@app.route('/about')
def about():
	return None

@app.route('/quizSelect')
def quizSelect():
	return render_template('quizSelect.html', quizzes = Quiz.query.all())

@app.route('/quiz/<string:quiz_name>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_name):
	print(quiz_name)
	quiz = None
	for quiz in Quiz.query.all():
		if quiz_name == quiz.short(): break
	quizStyle = quiz.quizStyle
	if session.get('quiz_id') == None:
		session['quiz_id'] = quiz.id
	elif session.get('quiz_id') != quiz.id:
		if session.get('question_id') != None: session.pop('question_id')
		session['quiz_id'] = quiz.id


	#If there isn't an attempt_id cookie
	if session.get('attempt_id') == None:
		#Start a new attempt
		userAttempts = current_user.get_user_quiz_attempts(quiz = quiz)
		lastUserAttempt = current_user.get_last_attempt(userAttempts = userAttempts)
		attemptNumber = 1
		if lastUserAttempt != None:
			attemptNumber = lastUserAttempt.attempt_number + 1
		newAttempt = UserAttempt(attempt_number = attemptNumber, user_id = current_user.id, quiz_id = quiz.id)
		db.session.add(newAttempt)
		db.session.commit()
		lastUserAttempt = current_user.get_last_attempt(userAttempts = userAttempts)
		session['attempt_id'] = lastUserAttempt.id

	#If there is a cookie telling us what question the user is up to
	if session.get('question_id') != None:
		question_id = session.get('question_id', None)
		question = quiz.questions.filter_by(id=question_id).first()
		form = make_form(quizStyle, question)
		submitted_form = request.form

		#If a form was submitted
		if submitted_form:
			submitted_choice = None
			if quizStyle.id == 1 :
				choices = question.question_choices
				submitted_choice = submitted_form.get('radioField')
				for choice in choices:
					if choice.choice_number == submitted_choice:
						submitted_choice = choice.id
						break
			elif quizStyle.id == 2:
				choices = question.question_choices
				submitted_choice = list(submitted_form.values())[1]
				for choice in choices:
					if choice.choice_content == submitted_choice:
						submitted_choice = choice.id
						break

			#Commit the answer to the DB
			print('Submitted choice:'+str(submitted_choice))
			if submitted_choice:
				answer = UserAnswer(user_id=current_user.id,question_id=question.id,choice_id=submitted_choice,attempt_id=session.get('attempt_id'))
				db.session.add(answer)
				db.session.commit()
				
				#Serve next question
				next_question = quiz.get_next_question(last_question = question)
				if next_question != None:
					session['question_id']=next_question.id
					next_form = make_form(quizStyle, next_question)
					return render_template(quizStyle.template_file,quiz = quiz,question = next_question,form = next_form)

				#Setup for results page
				session.pop('question_id', None)
				#Get UserAttempt objects
				user_attempts = current_user.get_user_quiz_attempts(quiz = quiz)
				attempt_list = user_attempts.all() #List may not be correctly ordered
				session_attempt_id = session.pop('attempt_id', None)
				this_attempt = None
				for this_attempt in attempt_list:
					if this_attempt.id == session_attempt_id:
						index = attempt_list.index(this_attempt)
						break
				attempt_number = this_attempt.attempt_number
				prev_score = None
				last_attempt = None
				if index > 0:
					last_attempt = attempt_list[index-1]
					prev_score = last_attempt.get_score()
				
				#Scores
				total_score = 0
				for attempt in user_attempts:
					total_score = total_score + attempt.get_score()
				average_score = round(total_score / user_attempts.count(),2)
				score = this_attempt.get_score()
				
				return render_template('landingpage.html',quiz = quiz, score = score, prev_score = prev_score, average_score = average_score, attempt_number = attempt_number )
		#if no form submitted or no choice made
		return render_template(quizStyle.template_file,quiz = quiz,question = question,form = form)
	#If starting from the beginning, no cookie
	question=quiz.get_question_by_question_number(question_number = 1)
	session['question_id'] = question.id
	form = make_form(quizStyle, question)
	return render_template(quizStyle.template_file,quiz = quiz,question = question,form = form)

def make_form(style, question):
	if style.id == 1:
		return StyleOneForm(question.get_question_choices_as_array_of_pairs())
	else :#style.id == 2:
		return StyleTwoForm(question.get_question_choices_as_array_of_pairs())

@app.route('/results')
@login_required
def results():
	answers = db.session.query(UserAnswer)
	choices = db.session.query(QuestionChoice)
	attempts = db.session.query(UserAttempt)
	attnum1 = 0
	attnum2 = 0
	score = 0
	score2 = 0

	for attempt in attempts:
		if attempt.quiz_id == 1:
			attnum1 = attnum1 + 1
		elif attempt.quiz_id == 2:
			attnum2 = attnum2 + 1
	

	for answer in answers:
				for choice in choices:
					if choice.id == answer.choice_id and choice.choice_correct == True and choice.question_id < 11:
						score = score + 1
					
	for answer in answers:
				for choice in choices:
					if choice.id == answer.choice_id and choice.choice_correct == True and choice.question_id > 10:
						score2 = score2 + 1

	average1 = round(score / attnum1,2)
	average2 = round(score2 / attnum2,2)

	
	

	return render_template('resultsall.html', attnum1 = attnum1, attnum2 = attnum2, average1 = average1, average2=average2)
