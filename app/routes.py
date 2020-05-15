from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
from app.models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


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
	return render_template('quizSelect.html')

@app.route('/quiz/<string:quiz_name>', methods=['GET', 'POST'])
def quiz(quiz_name):
	quiz = None
	if quiz_name == 'flag':
		quiz = Quiz.query.filter_by(quizname="Flag Quiz").first()
	elif quiz_name == 'lang':
		quiz = Quiz.query.filter_by(quizname="Language Quiz").first()
	quizStyle = quiz.quizStyle.template_file
	question=quiz.get_first_question()
	last_user_answer = current_user.get_last_answer(quiz = quiz)

	if last_user_answer != None:
		print(last_user_answer)
		question = quiz.get_next_question(last_user_answer = last_user_answer)

	if question is None:
		score = 0
		answers = db.session.query(UserAnswer)
		choices = db.session.query(QuestionChoice)
		for answers1 in answers:
			for choices1 in choices:
				if choices1.id == answers1.choice_id and choices1.choice_correct == True and answers1.user_id == current_user.id:
					score = score + 1
		return render_template('Results.html',quiz = quiz, score = score)
	
	form = None
	
	if quiz.quizStyle.style_name == 'Old flag style':
		choices = question.get_question_choices_as_array_of_pairs()
		form = StyleOneForm(choices,request.form)
	elif quiz.quizStyle.style_name == 'Language quiz style':
		choices = question.question_choices
		form = StyleTwoForm(choices,request.form)
	
	if form.is_submitted():
		answer = UserAnswer(user_id=current_user.id,question_id=question.id,choice_id=form.radioField.data)
		print("submitting: {}".format(answer))
		db.session.add(answer)
		db.session.commit()

	return render_template(quizStyle,quiz = quiz,question = question,form = form)

@app.route('/languageQuiz')
def languageQuiz():
	return render_template('HTML-languageQuizFinal.html')

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quiz, db.session))
admin.add_view(ModelView(QuizStyle, db.session))
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
