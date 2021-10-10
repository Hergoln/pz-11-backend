### Python version: 3.7

# Run project (command line)

1. Change directory to project folder.
2. Execute: `venv\Scripts\activate`
3. Set name of file to run app and environment
    1. set FLASK_APP=app (not needed, if main file is names app.py or wsgi.py)
    2. set FLASK_ENV=development (production default)
4. Run app: `flask run`

It should run on localhost.