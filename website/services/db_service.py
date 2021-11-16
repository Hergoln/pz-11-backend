from flask.blueprints import Blueprint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User('{self.username}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(60), nullable=False)

    def __repr__(self) -> str:
        return f"Post('{self.text}')"

def query_users(app):
    with app.app_context():
        print(User.query.all())