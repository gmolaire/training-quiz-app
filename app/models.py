import datetime
from . import db

def create_tables():
    db.create_all()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    answers = db.relationship('Answer', backref='user', lazy=True)
    score = db.Column(db.Integer, default=0)  # Track user's score
    completion_time = db.Column(db.Integer, nullable=True)  # Time taken in seconds

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.String(10), nullable=False)  # Change to String
    answer = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
