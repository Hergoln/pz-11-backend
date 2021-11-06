from flask import Flask
from flask_cors import CORS
from bots_battles import GameFactory

def create_app(game_factory: GameFactory) -> Flask:
    app = Flask(__name__)

    CORS(app, resources={
        r'/*': {
            'origins': '*'
        }
    })

    with app.app_context():
        
        from .services import basic_bp, game_bp
        import website.services as sv
        sv.init_factory(game_factory)
        
        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)
        return app