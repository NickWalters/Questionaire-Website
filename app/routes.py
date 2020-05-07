from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
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
	return redirect(url_for('index'))
	
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
	
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/quizSelect')
@login_required
def quizSelect():
	return render_template('quizSelect.html')

@app.route('/Flag')
def flag():
	quiz = Quiz.query.filter_by(quizname="Flag Quiz").first()
	quizStyle = quiz.quizStyle.template_file
	question = Question.query.filter_by(quiz_id=quiz.id).filter_by(question_number=1).first()
	return render_template(quizStyle,quiz = quiz,question = question)

@app.route('/languageQuiz')
def languageQuiz():
	return render_template('HTML-languageQuizFinal.html')
	
	

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Quiz, db.session))
admin.add_view(ModelView(Question, db.session))
admin.add_view(ModelView(QuestionChoice, db.session))
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