Project Plan:
1. Quiz content into DB
2. POST of quiz data to DB
3. Flask-Login (done?)
4. Flask-Admin
5. Migrate
6. Unit testing
7. DB drawings
8. README.md

Known issues:
1. IMG files > 5MB
2. Wrong links around the place
3. Change quizSelect to use DB (for quiz in Quiz.query.all())

Minor issues:
1. quizSelect border around images
2. User.get_last_answer(self, quiz) sucks

Optional extension:
1. Community polling - i.e. “what country are you from?” Or “how many languages do you speak?” And compare that to other users.
2. Serving quizzes via client-sided rendering w/ AJAX & JSON
3. Multiple answer types, checkbox/text
4. Randomised question sets