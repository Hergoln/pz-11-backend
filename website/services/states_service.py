import os
from flask import Blueprint, send_from_directory, current_app
from .db_service import db
from zipfile import ZipFile

states_bp = Blueprint("states", __name__)

@states_bp.route("/stts/<path:name>")
def download_file(name):
    with current_app.app_context():
        uploads = os.path.join(current_app.config['STARTING_PATH'], current_app.config['SAVED_STATES'])
        return send_from_directory(directory=uploads, path=name, as_attachment=True)

@states_bp.route("/stts-pckg/<gametype>")
def download_zipped(gametype):
    print(gametype)
    uploads = os.path.join(current_app.config['STARTING_PATH'], current_app.config['SAVED_STATES'])
    with ZipFile(os.path.join(uploads, 'sample2.zip'), 'w') as zippo, current_app.app_context():
        zippo.write(os.path.join(uploads, 'saved_state_01.txt'))
        return send_from_directory(directory=uploads, path='sample2.zip', as_attachment=True)