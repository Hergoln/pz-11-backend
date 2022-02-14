from typing import Optional
import os
from flask import render_template, Blueprint, send_from_directory, current_app

basic_bp = Blueprint("basic", __name__)

@basic_bp.route('/hello/')
@basic_bp.route('/hello/<name>')
def hello(name: Optional[str] =None):
    return render_template('hello.html', name=name)

@basic_bp.route("/uploads/<path:name>")
def download_file(name):
    with current_app.app_context():
        uploads = os.path.join(current_app.config['STARTING_PATH'], current_app.config['SAVED_STATES'])
        return send_from_directory(directory=uploads, path=name, as_attachment=True)