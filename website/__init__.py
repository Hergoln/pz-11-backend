from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r'/*': {
            'origins': '*'
        }
    })

    with app.app_context():
        from .services import basic_bp, game_bp

        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)
        return app