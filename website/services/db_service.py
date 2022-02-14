from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, current_app
from datetime import datetime, timedelta
import os

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    states_file_path = db.Column(db.String)
    type_id = db.Column(db.BigInteger)

    def __repr__(self) -> str:
        return f"Game('{self.id}', '{self.start_date}', '{self.end_date}', '{self.states_file_path}', '{self.type_id}')"

class GameType(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    type_name = db.Column(db.String)

    def __repr__(self) -> str:
        return f"GameType('{self.id}', '{self.type_name}')"

db_bp = Blueprint("db", __name__)

def init_db(app):
    app.register_blueprint(db_bp)
    db.init_app(app)
    db.create_all()

@db_bp.route('/add_game_to_db/')
def add_game_to_db():
    with current_app.app_context():
        start_date = datetime.today()
        end_date = datetime.today() + timedelta(hours=1)
        new_game = Game(start_date=start_date, end_date=end_date)
        db.session.add(new_game)
        db.session.commit()
        return new_game.__repr__()

@db_bp.route('/all_ended_games')
def all_ended_games():
    with current_app.app_context():
        return str(db.session.query(Game).all())