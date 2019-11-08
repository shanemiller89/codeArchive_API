# codeArchive API

Rest API for codeArchive

*** BEFORE YOU START, please make sure you have Python 3.7 or greater installed.

Clone Client side application and follow instructions. [Here](https://github.com/shanemiller89/codeArchive)

Clone this repository down in desired location:

```
git@github.com:shanemiller89/codeArchive_API.git
```

Enter these commands:

```
cd codearchive_API
python -m venv codearchiveEnv
source ./codearchive/bin/activate
```
Then run 

```
pip install -r requirements.txt
```

After installs are complete, run the following commands, in order.

```
python manage.py makemigrations codearchiveAPIapp
python manage.py migrate
python manage.py loaddata library_types
python manage.py loaddata log_types
python manage.py loaddata resource_types
python manage.py loaddata record_types
python manage.py runserver
```

Your codearchive API server is now up and running!

Run
```
python manage.py runserver
```
Each time you are using the application.

