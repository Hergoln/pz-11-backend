import os
from flask import Blueprint, send_from_directory, current_app, Response, jsonify
from .db_service import db
from zipfile import ZipFile
import io

states_bp = Blueprint("states", __name__)

possible_mappings = {'agarnt':['agarnt', "agarn't"]}

def resolve_mapping(gametype):
    gt = gametype.lower()
    for k, v in possible_mappings.items():
        if gt in v:
            return k
    return None


@states_bp.route("/stts/<path:name>")
def download_file(name):
    with current_app.app_context():
        uploads = os.path.join(current_app.config['STARTING_PATH'], current_app.config['SAVED_STATES'])
        return send_from_directory(directory=uploads, path=name, as_attachment=True)


@states_bp.route("/stts-pckg/<gametype>")
def download_zipped(gametype):
    states_dir = resolve_mapping(gametype)
    if states_dir is None:
        return jsonify({"message": f"gametype __{gametype}__ does not map to any known game"}), 404

    # zipp files
    requested_states_dir = os.path.join(
        current_app.config['STARTING_PATH'], 
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