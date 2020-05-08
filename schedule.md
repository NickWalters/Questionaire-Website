### Project Plan:
* <del>Quiz content into DB - Flag quiz
* Quiz content into DB - Language quiz
* <del>POST of quiz data to DB
* Flask-Login (done?)
* Flask-Admin
* Migrate
* Unit testing
* DB drawings
* README.md
* Results landing page

### Known issues:
* IMG files > 5MB
* Wrong links around the place
* Change quizSelect to use DB (for quiz in Quiz.query.all())

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