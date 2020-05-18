from app import app
import unittest
from app.models import User, Quiz, QuizContent, QuizStyle, Question, QuestionContent, QuestionChoice, UserAnswer
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
import os
from config import basedir


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()