from flask import render_template, flash, redirect, url_for, request, abort
from app import app, db
from werkzeug.urls import url_parse
from forms import LoginForm, RegistrationForm
from models import *
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	flash("Logged Out")
	return redirect(url_for('index'))
	
@app.route('/index')
def index():
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
def quizSelect():
	return render_template('quizSelect.html')
	
@app.route('/flag')
def flag():
	return render_template('flag.html')
	
@app.route('/languageQuiz')
def languageQuiz():
	return render_template('HTML-languageQuizFinal.html')