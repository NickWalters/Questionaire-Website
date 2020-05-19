from flask import render_template, flash, redirect, url_for, request, abort, session
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin


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
	quiz = None
	for quiz in Quiz.query.all():
		if quiz_name == quiz.short(): break
	quizStyle = quiz.quizStyle

	#If there is a cookie telling us what question the user is up to
	if session.get('question_number') != None:
		question_number = session.pop('question_number', None)
		question = quiz.get_question_by_question_number(question_number)
		form = make_form(quizStyle, question)
		submitted_form = request.form

		#If a form was submitted
		if submitted_form:
			submitted_choice = None
			if quizStyle.id == 1 :
				submitted_choice = submitted_form.get('radioField')
			elif quizStyle.id == 2:
				i = 0
				while i < form.len:
					choices_array = question.get_question_choices_as_array_of_pairs()
					if choices_array[i][1] == list(submitted_form.values())[0]:
						submitted_choice = i
						break
					i = i + 1
			#If any choice was given at all
			if submitted_choice != None:
				answer = UserAnswer(user_id=current_user.id,question_id=question.id,choice_id=submitted_choice)
				#Check this isn't a resubmitted form
				

				if True:
					#Commit the answer to the DB
					db.session.add(answer)
					db.session.commit()
					next_question = quiz.get_next_question(last_question = question)

					#If there are more questions to go
					if next_question != None:
						session['question_number']=next_question.question_number
						next_form = make_form(quizStyle, next_question)
						return render_template(quizStyle.template_file,quiz = quiz,question = next_question,form = next_form)
					score = 0
					answers = db.session.query(UserAnswer)
					choices = db.session.query(QuestionChoice)
					for answer in answers:
						for choice in choices:
							if choice.id == answer.choice_id and choice.choice_correct == True and answer.user_id == current_user.id:
								score = score + 1
					return render_template('results.html',quiz = quiz, score = score)
			#No choice in submitted form or it is a resubmitted form
			return render_template(quizStyle.template_file,quiz = quiz,question = question,form = form)
		#No form submitted
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
