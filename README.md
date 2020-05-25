README should describe:
1. the purpose of the web application, explaining both the context and the assessment mechanism used. 
2. the architecture of the web application 
3. describe how to launch the web application. 
4. describe some unit tests for the web application, and how to run them. 
5. Include commit logs, showing contributions and review from both contributing students

# Geography Quiz - Test your world knowledge
This flask application provides an architecture for multiple quizzes to be assigned to one database.
In this example, we have used a Geography Quiz, testing flag knowledge and how much you know about official languages.
This app provides functionality for:

- **User Registration and Log In** allowing users to log into our system securely (with hashing and validation) and access their previous scores, or any other allowed query with the database

- **Admins** Admin users can log into the page, change permissions of other users (admin or not) change user details, change questions, change question answers in the database, and look at the results of all the users in the database (who have submitted answers).

- **Results Page** Logged in users can see a summary of their results. Such as their average score, number of attempts, how much percentage improvement since last quiz (-% or +%) and their last raw score.

If users want to take a quiz, they must register an account. Users are 'unauthorized' to take a quiz without login information. After successful registration, there is a redirect and prompt on the login page. You can now use these registration details to log into your account. 
After log in, there is a welcome splash screen displayed to the user, outlining the various quizzes you can take.

## Authors
  * Nicholas Walters (22243339)
  * Nicholas Turner (21118739)
  * Sean Chu (22479185)
  * Rio Akbar


## Installation 
1:
**Install python3**

2:
**Enter the virtual environment by:**
```bash
virtualenv venv
source venv/bin/activate
```

To run a virtual environment on Windows, run the following commands:

```bash
virtualenv venv
venv\Scripts\activate
```

3:
**install the required files/packages (you must be in the project directory)**
```bash
pip install -r requirements.txt
```

4:
**Set path:**
Linux: 
```bash 
export FLASK_APP=app.py
```
Windows: 
```bash
set FLASK_APP=app.py
```

5:
**Run flask:**
```flask run```

**Running this command will start the website
You can access the website by visiting the provided link:**

http://127.0.0.1:5000/





If you are having problems with the virutal environment, do these steps:

Make a virtual environment in the project directory: 
python -m venv venv, or; python3 -m venv venv

2: Enter the virtual environment 
Linux by: source venv/bin/activate
Windows: venv/Scripts/activate


## Dependencies 
main packages:

`Flask`
`Flask-Admin`
`Flask-Login`
`Flask-SQLAlchemy`
`Flask-WTF`
`sqlalchemy-migrate`
`Flask-Migrate`

other packages:

`email-validator`
`itsdangerous`
`Jinja2`
`MarkupSafe`
`Werkzeug`

## Unit Testing and System/UserTesting

Unit tests can be performed by running python tests.py in the command line.



## References and Acknowledgements

The following tutorials were integral in learning Flask and building this application. Most modules were from the CITS3403 Laboratory Work. Comments are provided throughout the application indicating that a tutorial was followed to construct functions and features.

  * Miguel Grindberg's "Flask Mega-Tutorial, Chapters 1-8". Found at: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world. 
