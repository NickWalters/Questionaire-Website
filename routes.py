from flask import render_template, flash, redirect
from app import app
from forms import LoginForm, RegistrationForm
from models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)
	

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
def quizSelect():
	return render_template('quizSelect.html')
	
	
@app.route('/flag')
def flag():
	return render_template('flag.html')
	

@app.route('/languageQuiz')
def languageQuiz():
	return render_template('HTML-languageQuizFinal.html')