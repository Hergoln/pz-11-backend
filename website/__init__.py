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
        app.config['SAVED_STATES'] = os.environ.get('SAVED_STATES', os.path.join('bots_battles', 'games', 'states'))
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///memory.db')
        app.config['STARTING_PATH'] = os.path.dirname(os.path.abspath(__file__))

        from .services import basic_bp, game_bp, init_db, init_states
        import website.services as sv
        sv.init_game_server(game_server)
        
        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)

        init_states(app)
        init_db(app)

        return app