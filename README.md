#Installing as per mega tutorial with venv

Install python

Make a virtual environment in the project directory:
python -m venv venv, or;
python3 -m venv venv

Enter the virtual environment 
Linux: source venv/bin/active
Windows: venv/Scripts/active

--- Alternative (Mac or linux)
virtualenv env -p python3
source env/bin/activate


Install flask and the allowed libraries in the virtual environment (venv):
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate

Set path:
Linux: export FLASK_APP:app.py
Windows: set FLASK_APP=app.py

Run flask:
flask run, or;
python app.py, or;
python3 app.py

Running this command will start the website
You can access the website by visiting the provided link:

http://127.0.0.1:5000/
