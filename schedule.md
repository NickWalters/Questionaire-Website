### Project Requirements:
* <del>Quiz content into DB - Flag quiz
* <del>Quiz content into DB - Language quiz
* <del>POST of quiz data to DB
* <del>Flask-Login (done?)
* <del>Migrate
* Flask-Admin - fix up individual pages
* Unit testing
* DB drawings - dbSchema.xlsx
* README.md
* Results landing page

### Known issues:
* Flash and alerts not functional
* <del>IMG files > 5MB
* Section 2 of home page, 'SAMPLE TEST'
* About page
* Form validation on quizzes - reject empty forms + check form data is valid
* Will proceed to next question even if the answer failed to commit to DB
* <del>Change quizSelect to use DB (for quiz in Quiz.query.all())
* <del>AttributeError: 'AnonymousUserMixin' object has no attribute 'get_last_answer' when attempting to do a quiz without being loged in
* <del>Quiz blurb variable in DB
* <del>Takes submitting question 1 multiple times
* <del>Question 10 not submitting -> form issue
* <del>Unauthorized, should boot to login page not

### Minor flawed implementations:
* User.get_last_answer(self, quiz) is hacky
* Style2 form generation is hacky

### Minor cosmetic issues:
* quizSelect border around images
* Style problems from when everything was moved over to templates
* Buttons on language quiz style

### Optional extension:
* Community polling - i.e. “what country are you from?” Or “how many languages do you speak?” And compare that to other users.
* Serving quizzes via client-sided rendering w/ AJAX & JSON
* Multiple answer types, checkbox/text
* Randomised question sets
* quiz.allow_multiple_attempts
* quiz.must_complete_attempts
* timer
* leaderboards

### Reference for Images
banner.jpg
- https://unsplash.com/photos/jCBzW_Q_UGI
Overlay.png
- https://www.pexels.com/photo/beige-analog-gauge-697662/
Flag quiz - all .svg
- http://hjnilsson.github.io/country-flags/