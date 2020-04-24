from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = 'static'

import routes

if __name__ == '__main__':
	app.run() # for debug mode, Modify to app.run(debug=True).

