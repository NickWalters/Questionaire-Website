from flask import render_template
from app import app

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