#Installing as per mega tutorial with venv

1:
Install python and pip

2:
Enter the virtual environment by:
```virtualenv env -p python3```
```source env/bin/activate```

3:
install the required files/packages (you must be in the project directory)
```pip install -r requirements.txt```

4:
Set path:
Linux: export ```FLASK_APP:app.py```
Windows: set ```FLASK_APP=app.py```

5:
Run flask:
```flask run```

Running this command will start the website
You can access the website by visiting the provided link:

http://127.0.0.1:5000/





If you are having problems with the virutal environment, do these steps:

Make a virtual environment in the project directory: 
python -m venv venv, or; python3 -m venv venv

2: Enter the virtual environment 
Linux by: virtualenv env -p python3 source venvenv/bin/active 
Windows: venv/Scripts/activate

