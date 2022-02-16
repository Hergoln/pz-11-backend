import os
from flask import Blueprint, send_from_directory, current_app, Response, jsonify
from .db_service import db
from zipfile import ZipFile
import io
from settings import GAMES_NAMES_MAPPING

states_bp = Blueprint("states", __name__)

def resolve_mapping(gametype):
    gt = gametype.lower()
    for k, v in GAMES_NAMES_MAPPING.items():
        if gt in v or gt == k:
            return k
    return None

# have to be run after config value 'SAVED_STATES' has been initialized
def init_states(app):
    app.register_blueprint(states_bp)
    # create directories
    states_path = current_app.config['SAVED_STATES']
    if not os.path.exists(states_path):
        os.makedirs(states_path)
        for dir in GAMES_NAMES_MAPPING.keys():
            os.makedirs(os.path.join(states_path, dir))

@states_bp.route("/stts/<path:name>")
def download_file(name):
    with current_app.app_context():
        return send_from_directory(
            directory=current_app.config['SAVED_STATES'], 
            path=name, as_attachment=True)


@states_bp.route("/stts-pckg/<gametype>")
def download_zipped(gametype):
    states_dir = resolve_mapping(gametype)
    if states_dir is None:
        return jsonify({"message": f"gametype __{gametype}__ does not map to any known game"}), 404

    # zipp files
    requested_states_dir = os.path.join(
        current_app.config['SAVED_STATES'], 
        states_dir)
    data = io.BytesIO()
    with ZipFile(data, 'w') as zippo:
        for file in os.listdir(requested_states_dir):
            zippo.write(os.path.join(requested_states_dir, file), arcname=file)
    data.seek(0)

    with current_app.app_context():
        return Response(data.getvalue(), 
        mimetype='application/zip', 
        headers={'Content-Disposition': f"attachment;filename={states_dir}.zip"})