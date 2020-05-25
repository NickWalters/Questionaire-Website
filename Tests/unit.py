import os
import unittest
from app import app, db
from app.models import User, Quiz, QuizContent, QuizStyle, Question, QuestionContent, QuestionChoice, UserAnswer
from app.forms import LoginForm, RegistrationForm, StyleOneForm, StyleTwoForm
from config import basedir

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #Helper Functions

    def register(self, username, email, password, password2):
        return self.app.post("/register", data=dict(username=username, 
        email=email,
        password=password,
        password2=password2),
        follow_redirects = True)
    
    def  login(self, username, password):
        return self.app.post("/login", data=dict(username=username,
        password=password), follow_redirects = True)

    def logout(self):
        return self.app.get('/logout', follow_redirects = True)
    
    def nextQuestionFlag(self, radiofield):
        return self.app.post('/quiz/flag', data=dict(radioField = radiofield), follow_redirects = True)

    def nextLanguageFlag(self, radiofield):
        return self.app.post('/quiz/language', data=dict(radioField = radiofield), follow_redirects = True)



#Registration Functionality Tests
    #tests a valid registration attempt
    def test_valid_registration(self):
        response = self.register("user", "user@email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Log In</title>', response.data)

    #Tests an invalid registration attempt where passwords do not match
    def test_invalid_registration_passwords(self):
        response = self.register("user", "grae@email.com", "password", "invalid password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)

    #Tests an invalid registration attempt where email is invalid
    def test_invalid_registration_email(self):
        #missing @ symbol
        response = self.register("user", "invalid email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)

        #missing domain
        response = self.register("user", "invalid@email", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)

        #invalid space inserted
        response = self.register("user", "invalid@ email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)

    #Tests an invalid registration where the username and/or email are already taken
    def test_invalid_registration_duplicates(self):
        u1 = User(username = "existing_user", email = "existing_user@email.com", password_hash = "User.set_password('password')")
        db.session.add(u1)
        db.session.commit()

        #duplicate username
        response = self.register("existing_user", "user@email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User name has been used', response.data)

        #duplicate email
        response = self.register("user", "existing_user@email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email has been used', response.data)
    
    #Tests an invalid registration where one of the fields has been left blank
    def test_invalid_registration_missing(self):
        response = self.register("", "user@email.com", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data) #redirected to register page
        self.assertIn(b'value=""', response.data) #at least 1 field has been left empty

        response = self.register("user", "", "password", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

        response = self.register("user", "user@email.com", "", "password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

        response = self.register("user", "user@email.com", "password", "")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Register</title>', response.data)
        self.assertIn(b'value=""', response.data)

#LOGIN FUNCTIONALITY TESTS
    #Tests a valid login 
    def test_successful_login(self):
        user = User(username="bob", email="bob@email.com")
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        db.session.add(user)
        db.session.commit()

        response = self.login("bob", "password")
        self.assertIn(b'Hello bob!', response.data)
        self.assertIn(b'<title>Questionaire - How do you Compare?</title>', response.data)
    
    #Tests invalid login attempts
    def test_unsuccussful_login(self):
        user = User(username="bob", email="bob@email.com")
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        db.session.add(user)
        db.session.commit()

        #invalid username or password
        response = self.login("bob", "invalid")
        self.assertIn(b'<title>Log In</title>', response.data)

        response = self.login("invalid", "password")
        self.assertIn(b'<title>Log In</title>', response.data)
        
        #username or password missing
        response = self.login("", "password")
        self.assertIn(b'<title>Log In</title>', response.data)

        response = self.login("bob", "")
        self.assertIn(b'<title>Log In</title>', response.data)

#LOGOUT FUNCTIONALITY TESTS:
    #test logout
    def test_logout(self):
        self.app.get('/register', follow_redirects = True)
        self.register("user", "user@email.com", "password", "password")
        self.app.get('/login', follow_redirects = True)
        self.login("user", "password")
        response = self.app.get('/logout', follow_redirects = True)
        self.assertIn(b'Please Login to save your scores', response.data)

#ADMIN TESTS:
    #successful login as admin
    def test_admin_login(self):
        user = User(username="john", email="john@email.com")
        user.set_password('password')
        user.admin = True
        db.session.add(user)
        db.session.commit()

        response = self.login("john", "password")
        self.assertIn(b'Hello Admin john!', response.data)

    #unsuccessful login as admin
    def test_nonadmin_login(self):
        user = User(username="john", email="john@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()

        response = self.login("john", "password")
        self.assertNotIn(b'Hello Admin john!', response.data)

    #accessing the flag quiz if not logged in
    def test_flagquiz_not_logged_in(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()
        self.login("user", "password")
        self.app.get('/logout', follow_redirects = True)
        response = self.app.get('/quiz/flag', follow_redirects = True)
        self.assertIn(b'<title>Log In</title>', response.data)

    #accessing the language quiz if not logged in
    def test_languagequiz_not_logged_in(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()
        self.login("user", "password")
        self.app.get('/logout', follow_redirects = True)
        response = self.app.get('/quiz/language', follow_redirects = True)
        self.assertIn(b'<title>Log In</title>', response.data)

    #access the results page test
    def test_access_results_page_logged_in(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()
        self.login("user", "password")
        response = self.app.get('/results', follow_redirects = True)
        self.assertIn(b'<title>results</title>', response.data)
    
    #access the results page, not logged in
    def test_access_results_page_not_logged(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.commit()
        self.login("user", "password")
        self.app.get('/logout', follow_redirects = True)
        response = self.app.get('/results', follow_redirects = True)
        self.assertIn(b'<title>Log In</title>', response.data)


    def test_language_quiz(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.add(Quiz(quizname="Language Quiz",creator_id=1,style=2))
        db.session.add(QuizStyle(style_name="Language quiz style",template_file="quizStyle2.html")) 
        db.session.add(QuizContent(quiz_id=2,text_content="How much do you know about world culture, information and languages?",img_content="people-banner.png"))
        db.session.add(Question(quiz_id=2,question_number=1))
        db.session.add(Question(quiz_id=2,question_number=2))
        db.session.add(Question(quiz_id=2,question_number=3))
        db.session.add(Question(quiz_id=2,question_number=4))
        db.session.add(Question(quiz_id=2,question_number=5))
        db.session.add(Question(quiz_id=2,question_number=6))
        db.session.add(Question(quiz_id=2,question_number=7))
        db.session.add(Question(quiz_id=2,question_number=8))
        db.session.add(Question(quiz_id=2,question_number=9))
        db.session.add(Question(quiz_id=2,question_number=10))
        db.session.add(QuestionContent(question_id=11,text_content="What is the Official Language of Taiwan",img_content="taiwan-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=12,text_content="What is the Official Language of Australia",img_content="australia-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=13,text_content="What is the Official Language of Norway",img_content="norway-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=14,text_content="What is the Official Language of Colombia",img_content="colombia-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=15,text_content="What is the Official Language of Pakistan",img_content="pakistan-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=16,text_content="What is the Official Language of Ukraine",img_content="ukraine-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=17,text_content="What is the Official Language of Malaysia",img_content="malaysia-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=18,text_content="What is the Official Language of Mexico",img_content="mexico-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=19,text_content="What is the Official Language of Iran",img_content="iran-languageQuiz.jpg"))
        db.session.add(QuestionContent(question_id=20,text_content="What is the Official Language of Indonesia",img_content="indonesia-languageQuiz.jpg"))
        db.session.add(QuestionChoice(question_id=11,choice_number=1,choice_content="Taiwanese",choice_correct=False))
        db.session.add(QuestionChoice(question_id=11,choice_number=2,choice_content="Japanese",choice_correct=False))
        db.session.add(QuestionChoice(question_id=11,choice_number=3,choice_content="Mandarin",choice_correct=True))
        db.session.add(QuestionChoice(question_id=11,choice_number=4,choice_content="Cantonese",choice_correct=False))
        db.session.add(QuestionChoice(question_id=12,choice_number=1,choice_content="English",choice_correct=True))
        db.session.add(QuestionChoice(question_id=12,choice_number=2,choice_content="German",choice_correct=False))
        db.session.add(QuestionChoice(question_id=12,choice_number=3,choice_content="Korean",choice_correct=False))
        db.session.add(QuestionChoice(question_id=12,choice_number=4,choice_content="Russian",choice_correct=False))
        db.session.add(QuestionChoice(question_id=13,choice_number=1,choice_content="German",choice_correct=False))
        db.session.add(QuestionChoice(question_id=13,choice_number=2,choice_content="Spanish",choice_correct=False))
        db.session.add(QuestionChoice(question_id=13,choice_number=3,choice_content="English",choice_correct=False))
        db.session.add(QuestionChoice(question_id=13,choice_number=4,choice_content="Romani",choice_correct=True))  
        db.session.add(QuestionChoice(question_id=14,choice_number=1,choice_content="Spanish",choice_correct=True))
        db.session.add(QuestionChoice(question_id=14,choice_number=2,choice_content="Irish",choice_correct=False))
        db.session.add(QuestionChoice(question_id=14,choice_number=3,choice_content="Dutch",choice_correct=False))
        db.session.add(QuestionChoice(question_id=14,choice_number=4,choice_content="French",choice_correct=False))
        db.session.add(QuestionChoice(question_id=15,choice_number=1,choice_content="Perish",choice_correct=False))
        db.session.add(QuestionChoice(question_id=15,choice_number=2,choice_content="Hindi",choice_correct=False))
        db.session.add(QuestionChoice(question_id=15,choice_number=3,choice_content="Arabic",choice_correct=False))
        db.session.add(QuestionChoice(question_id=15,choice_number=4,choice_content="Urdu",choice_correct=True))
        db.session.add(QuestionChoice(question_id=16,choice_number=1,choice_content="Ukrainian",choice_correct=True))
        db.session.add(QuestionChoice(question_id=16,choice_number=2,choice_content="Russian",choice_correct=False))
        db.session.add(QuestionChoice(question_id=16,choice_number=3,choice_content="Greenlandic",choice_correct=False))
        db.session.add(QuestionChoice(question_id=16,choice_number=4,choice_content="Galician",choice_correct=False))
        db.session.add(QuestionChoice(question_id=17,choice_number=1,choice_content="Malaysian",choice_correct=False))
        db.session.add(QuestionChoice(question_id=17,choice_number=2,choice_content="Malayense",choice_correct=False))
        db.session.add(QuestionChoice(question_id=17,choice_number=3,choice_content="Mandarin",choice_correct=False))
        db.session.add(QuestionChoice(question_id=17,choice_number=4,choice_content="Malay",choice_correct=True))
        db.session.add(QuestionChoice(question_id=18,choice_number=1,choice_content="Spanish",choice_correct=True))
        db.session.add(QuestionChoice(question_id=18,choice_number=2,choice_content="Mexian",choice_correct=False))
        db.session.add(QuestionChoice(question_id=18,choice_number=3,choice_content="Portuguese",choice_correct=False))
        db.session.add(QuestionChoice(question_id=18,choice_number=4,choice_content="Welsh",choice_correct=False))
        db.session.add(QuestionChoice(question_id=19,choice_number=1,choice_content="Arabic",choice_correct=False))
        db.session.add(QuestionChoice(question_id=19,choice_number=2,choice_content="Hebrew",choice_correct=False))
        db.session.add(QuestionChoice(question_id=19,choice_number=3,choice_content="Persian",choice_correct=True))
        db.session.add(QuestionChoice(question_id=19,choice_number=4,choice_content="Hindi",choice_correct=False))
        db.session.add(QuestionChoice(question_id=20,choice_number=1,choice_content="Malay",choice_correct=False))
        db.session.add(QuestionChoice(question_id=20,choice_number=2,choice_content="Indonesia",choice_correct=True))
        db.session.add(QuestionChoice(question_id=20,choice_number=3,choice_content="Mandarin",choice_correct=False))
        db.session.add(QuestionChoice(question_id=20,choice_number=4,choice_content="Thai",choice_correct=False))
        db.session.commit()
        self.login("user", "password")
        self.app.get('/quiz/language', follow_redirects = True)
        self.nextLanguageFlag("Mandarin")
        response = self.nextLanguageFlag("English")
        self.assertIn(b'<img src="/static/images/australia-languageQuiz.jpg" alt="map" id="image">', response.data)

    def test_flag_quiz(self):
        user = User(username="user", email="user@email.com")
        user.set_password('password')
        user.admin = False
        db.session.add(user)
        db.session.add(Quiz(quizname="Flag Quiz",creator_id=1,style=1))
        db.session.add(QuizStyle(style_name="Old flag style",template_file="quizStyle1.html"))
        db.session.add(QuizContent(quiz_id=1,text_content="Are you truly aware of the outside world? Do you have what it takes to test your knowledge on the flags of the world? Take our test !",img_content="au.svg"))
        db.session.add(Question(quiz_id=1,question_number=1))
        db.session.add(Question(quiz_id=1,question_number=2))   
        db.session.add(Question(quiz_id=1,question_number=3))
        db.session.add(Question(quiz_id=1,question_number=4))
        db.session.add(Question(quiz_id=1,question_number=5))
        db.session.add(Question(quiz_id=1,question_number=6))
        db.session.add(Question(quiz_id=1,question_number=7))
        db.session.add(Question(quiz_id=1,question_number=8))
        db.session.add(Question(quiz_id=1,question_number=9))
        db.session.add(Question(quiz_id=1,question_number=10))
        db.session.add(QuestionContent(question_id=1,text_content="What country flag is this?",img_content="flag01.svg"))
        db.session.add(QuestionContent(question_id=2,text_content="What country flag is this?",img_content="flag02.svg"))
        db.session.add(QuestionContent(question_id=3,text_content="What country flag is this?",img_content="flag03.svg"))
        db.session.add(QuestionContent(question_id=4,text_content="What country flag is this?",img_content="flag04.svg"))
        db.session.add(QuestionContent(question_id=5,text_content="What country flag is this?",img_content="flag05.svg"))
        db.session.add(QuestionContent(question_id=6,text_content="What country flag is this?",img_content="flag06.svg"))
        db.session.add(QuestionContent(question_id=7,text_content="What country flag is this?",img_content="flag07.svg"))
        db.session.add(QuestionContent(question_id=8,text_content="What country flag is this?",img_content="flag08.svg"))
        db.session.add(QuestionContent(question_id=9,text_content="What country flag is this?",img_content="flag09.svg"))
        db.session.add(QuestionContent(question_id=10,text_content="What country flag is this?",img_content="flag10.svg"))
        db.session.add(QuestionChoice(question_id=1,choice_number=1,choice_content="Namibia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=1,choice_number=2,choice_content="Turks and Caicos Islands",choice_correct=False))
        db.session.add(QuestionChoice(question_id=1,choice_number=3,choice_content="Mongolia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=1,choice_number=4,choice_content="Saint Pierre and Miquelon",choice_correct=True))
        db.session.add(QuestionChoice(question_id=2,choice_number=1,choice_content="French Polynesia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=2,choice_number=2,choice_content="Maldives",choice_correct=False))
        db.session.add(QuestionChoice(question_id=2,choice_number=3,choice_content="Djibouti",choice_correct=False))
        db.session.add(QuestionChoice(question_id=2,choice_number=4,choice_content="Botswana",choice_correct=True))
        db.session.add(QuestionChoice(question_id=3,choice_number=1,choice_content="Anguilla",choice_correct=False))
        db.session.add(QuestionChoice(question_id=3,choice_number=2,choice_content="Lesotho",choice_correct=False))
        db.session.add(QuestionChoice(question_id=3,choice_number=3,choice_content="Western Sahara",choice_correct=False))
        db.session.add(QuestionChoice(question_id=3,choice_number=4,choice_content="Gabon",choice_correct=True))
        db.session.add(QuestionChoice(question_id=4,choice_number=1,choice_content="Heard Island and McDonald Islands",choice_correct=False))
        db.session.add(QuestionChoice(question_id=4,choice_number=2,choice_content="American Samoa",choice_correct=False))
        db.session.add(QuestionChoice(question_id=4,choice_number=3,choice_content="Zimbabwe",choice_correct=False))
        db.session.add(QuestionChoice(question_id=4,choice_number=4,choice_content="Puerto Rico",choice_correct=True))
        db.session.add(QuestionChoice(question_id=5,choice_number=1,choice_content="Isle of Man",choice_correct=False))
        db.session.add(QuestionChoice(question_id=5,choice_number=2,choice_content="South Georgia and the South Sandwich Islands",choice_correct=False))
        db.session.add(QuestionChoice(question_id=5,choice_number=3,choice_content="Iran",choice_correct=False))
        db.session.add(QuestionChoice(question_id=5,choice_number=4,choice_content="Pitcairn",choice_correct=True))
        db.session.add(QuestionChoice(question_id=6,choice_number=1,choice_content="Korea (Republic of)",choice_correct=False))
        db.session.add(QuestionChoice(question_id=6,choice_number=2,choice_content="Cayman Islands",choice_correct=False))
        db.session.add(QuestionChoice(question_id=6,choice_number=3,choice_content="Myanmar",choice_correct=False))
        db.session.add(QuestionChoice(question_id=6,choice_number=4,choice_content="Kiribati",choice_correct=True))
        db.session.add(QuestionChoice(question_id=7,choice_number=1,choice_content="Slovenia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=7,choice_number=2,choice_content="Brunei",choice_correct=False))
        db.session.add(QuestionChoice(question_id=7,choice_number=3,choice_content="Saint Martin (French part)",choice_correct=False))
        db.session.add(QuestionChoice(question_id=7,choice_number=4,choice_content="Suriname",choice_correct=True))
        db.session.add(QuestionChoice(question_id=8,choice_number=1,choice_content="Finland",choice_correct=False))
        db.session.add(QuestionChoice(question_id=8,choice_number=2,choice_content="Fiji",choice_correct=False))
        db.session.add(QuestionChoice(question_id=8,choice_number=3,choice_content="Bahamas",choice_correct=False))
        db.session.add(QuestionChoice(question_id=8,choice_number=4,choice_content="Colombia",choice_correct=True))
        db.session.add(QuestionChoice(question_id=9,choice_number=1,choice_content="Rwanda",choice_correct=False))
        db.session.add(QuestionChoice(question_id=9,choice_number=2,choice_content="Georgia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=9,choice_number=3,choice_content="Palestine",choice_correct=False))
        db.session.add(QuestionChoice(question_id=9,choice_number=4,choice_content="Czechia",choice_correct=True))
        db.session.add(QuestionChoice(question_id=10,choice_number=1,choice_content="Afghanistan",choice_correct=False))
        db.session.add(QuestionChoice(question_id=10,choice_number=2,choice_content="Indonesia",choice_correct=False))
        db.session.add(QuestionChoice(question_id=10,choice_number=3,choice_content="Angola",choice_correct=False))
        db.session.add(QuestionChoice(question_id=10,choice_number=4,choice_content="Jersey",choice_correct=True))
        db.session.commit()
        self.login("user", "password")
        self.app.get('/quiz/flag', follow_redirects = True)
        self.nextQuestionFlag("Saint Pierre and Miquelon")
        self.nextQuestionFlag("Botswana")
        self.nextQuestionFlag("Gabon")
        self.nextQuestionFlag("Puerto Rico")
        self.nextQuestionFlag("Pitcairn")
        self.nextQuestionFlag("Kiribati")
        self.nextQuestionFlag("Suriname")
        self.nextQuestionFlag("Colombia")
        response = self.nextQuestionFlag("Czechia")
        self.assertIn(b'src="/static/images/flag10.svg', response.data)

    
        



if __name__ == '__main__':
    unittest.main()
