from flask import render_template, flash, redirect
from app import app
from forms import LoginForm

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
			form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)
	
@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/quizSelect')
def quizSelect():
	return render_template('quizSelect.html')
	
@app.route('/world')
def world():
	return render_template('world.html')
	
@app.route('/flag')
def flag():
	return render_template('flag.html')