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
        
        from .services import basic_bp, game_bp, states_bp, init_db
        import website.services as sv
        sv.init_game_server(game_server)
        
        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)
        app.register_blueprint(states_bp)

        sqlite_default = 'sqlite:///memory.db'
        app.config['SAVED_STATES'] = os.path.join('bots_battles', 'games', 'states')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', sqlite_default)
        init_db(app)

        return app