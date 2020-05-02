from app import app, db
from models import User, Question, QuestionChoice, UserAnswer


@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Question': Question, 'QuestionChoices': QuestionChoice, 'UserAnswer': UserAnswer}

