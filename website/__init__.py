from flask import Flask
from flask_cors import CORS
from bots_battles import GameFactory, GameServer
import os

def create_app(game_server: GameServer, game_factory: GameFactory) -> Flask:
    app = Flask(__name__)

    CORS(app, resources={
        r'/*': {
            'origins': '*'
        }
    })

    with app.app_context():
        
        from .services import basic_bp, game_bp, db
        import website.services as sv
        sv.init_game_server(game_server)
        
        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///:memory:')
        db.init_app(app)

        return app