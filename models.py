from app import db
from datetime import datetime
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import os

class User(db.Model):
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(64), index=True, unique=True)
		email = db.Column(db.String(120), index=True, unique=True)
		admin = db.Column(db.Boolean, default=False, nullable=False) 
		password_hash = db.Column(db.String(128))
		# scores = db.relationship('Result', backref'user', lazy="dynamic")
		

		def is_admin(self):
			return self.admin

		def set_password(self, password):
			self.password_hash = generate_password_hash(password)

		def check_password(self, password):
			return check_password_hash(self.password_hash, password)

		def __repr__(self):
			print('<admin or not {}>'.format(self.admin))
			return '{}'.format(self.username)
			
			
			

# this is an attempt of a quiz. The date and data scoresheet has been recorded	
class Result(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	
	flagQuiz = db.Column(db.Boolean, default=False)
	worldQuiz = db.Column(db.Boolean, default=False)
	score = db.Column(db.Integer)
	date_of_attempt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	
	

# create sample users
db.drop_all()
db.create_all()

user_1 = User(username="JohnDoe", email="John@hotmail.com", admin=False, password_hash="notASecret")

user_2 = User(username="Nick", email="nick@gmail.com", admin=True, password_hash="blahblah")


db.session.add(user_1)
db.session.add(user_2)

users = User.query.all()
print(users)

db.session.commit()

