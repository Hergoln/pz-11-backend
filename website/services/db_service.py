from flask.blueprints import Blueprint
from flask_sqlalchemy import SQLAlchemy
from typing import Optional
from flask import render_template, jsonify, Blueprint, current_app
from datetime import datetime, timedelta

db = SQLAlchemy()

class Game(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    states_id = db.Column(db.BigInteger)
    type_id = db.Column(db.BigInteger)

    def __repr__(self) -> str:
        return f"Game('{self.id}', '{self.start_date}', '{self.end_date}', '{self.states_id}', '{self.type_id}')"

class GameStates(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    states_id = db.Column(db.JSON)

    def __repr__(self) -> str:
        return f"GameStates('{self.id}', '{self.states_id}')"

class GameType(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    type_name = db.Column(db.String)

    def __repr__(self) -> str:
        return f"GameType('{self.id}', '{self.type_name}')"

db_bp = Blueprint("db", __name__)

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