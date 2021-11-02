from flask import Flask
from flask_cors import CORS

from bots_battles.game_engine.networking.game_server import GameServer
from bots_battles.games.game_factory import GameFactory

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