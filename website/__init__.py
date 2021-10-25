from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from .services import basic_bp, game_bp

        app.register_blueprint(basic_bp)
        app.register_blueprint(game_bp)
        return app