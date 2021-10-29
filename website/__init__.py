from flask import Flask

from bots_battles.game_engine.networking.game_server import GameServer
from bots_battles.games.game_factory import GameFactory

def create_app():
    app = Flask(__name__)
    # ws_app = GameServer(GameFactory(), 'localhost', 5001)

    with app.app_context():
        from .services import basic_bp, game_bp

        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)
        return app