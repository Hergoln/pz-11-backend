### Python version: 3.7

# Run project (command line)

1. Change directory to project folder.
2. Create virtual environment folder: `py -3 -m venv venv` (if not existing).
3. Execute: `venv\Scripts\activate`
4. Install flask: `pip install Flask` (if not installed)
4. Set name of file to run app and environment
    1. set FLASK_APP=app (not needed, if main file is names app.py or wsgi.py)
    2. set FLASK_ENV=development (production default)
    3. set FLASK_DEBUG=1 (debug mode off default)
5. Run app: `flask run`

It should run on localhost.