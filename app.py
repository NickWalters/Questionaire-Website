from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = 'static'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

import routes, models

if __name__ == '__main__':
	app.run() # for debug mode, Modify to app.run(debug=True).
	
	
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Question': Question, 'QuestionChoices': QuestionChoices, 'UserAnswer': UserAnswer, 'Result': Result}

