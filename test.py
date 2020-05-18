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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #Helper Functions

    def register(self, username, email, password, password2, submit):
        return self.app.post("/register", data=dict(username=username, 
        email=email,
        password=password,
        password2=password2),
        follow_redirects = True)

#Registration Functionality Tests
    #tests a valid registration attempt
    def test_valid_registration(self):
        response = self.register("user", "user@email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

    #Tests an invalid registration attempt where passwords do not match
    def test_invalid_registration_passwords(self):
        response = self.register("user", "grae@email.com", "password", "invalid password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Field must be equal to password', response.data)

    #Tests an invalid registration attempt where email is invalid
    def test_invalid_registration_email(self):
        #missing @ symbol
        response = self.register("user", "invalid email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)

        #missing domain
        response = self.register("user", "invalid@email", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)

        #invalid space inserted
        response = self.register("user", "invalid@ email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address', response.data)