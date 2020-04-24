# Installing venv as per MiguelGrinberg flask mega tutorial
Install instructions

Install python, I used windows store Python 3.8

Start a virtual environment:
python -m venv venv
Linux: source venv/bin/active
Windows: venv/Scripts/activate

Now install flask in the virtual environment (venv):
pip install flask

Set path
LINUX: export FLASK_APP=qsite.py
Windows: set FLASK_APP=qsite.py

flask run