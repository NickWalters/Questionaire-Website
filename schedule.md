### Github Meeting:

### Project Plan:
* <del>Quiz content into DB - Flag quiz
* Quiz content into DB - Language quiz
* <del>POST of quiz data to DB
* Flask-Login (done?)
* Flask-Admin - fix up individual pages
* Migrate
* Unit testing
* DB drawings - dbSchema.xlsx
* README.md
* Results landing page 

### Known issues:
* IMG files > 5MB
* Wrong links around the place
* Change quizSelect to use DB (for quiz in Quiz.query.all())
* AttributeError: 'AnonymousUserMixin' object has no attribute 'get_last_answer'
* Takes submitting question 1 multiple times
* Question 10 not submitting -> form issue

### Minor issues:
* quizSelect border around images
* User.get_last_answer(self, quiz) is hacky

### Optional extension:
* Community polling - i.e. “what country are you from?” Or “how many languages do you speak?” And compare that to other users.
* Serving quizzes via client-sided rendering w/ AJAX & JSON
* Multiple answer types, checkbox/text
* Randomised question sets
* quiz.allow_multiple_attempts
* quiz.must_complete_attempts
* timer
* leaderboards

Reference for Images
banner.jpg
- https://unsplash.com/photos/jCBzW_Q_UGI
Overlay.png
- https://www.pexels.com/photo/beige-analog-gauge-697662/