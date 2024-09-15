from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, Answer
from .quiz import QUESTIONS
from . import db
import time

quiz_bp = Blueprint('quiz_bp', __name__)

@quiz_bp.route('/thank_you/<username>')
def thank_you(username):
    return render_template('thank_you.html', username=username)

@quiz_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        session['username'] = username  # Store username in session
        session['start_time'] = time.time()  # Track start time
        return redirect(url_for('quiz_bp.quiz', username=username))
    return render_template('index.html')

@quiz_bp.route('/quiz/<username>', methods=['GET', 'POST'])
def quiz(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if not user:
            return "User not found", 404

        user.score = 0
        for question_id, answer in request.form.items():
            new_answer = Answer(user_id=user.id, question_id=question_id, answer=answer)
            if answer.lower() == QUESTIONS[question_id]['correct_answer'].lower():
                new_answer.is_correct = True
                user.score += 1
            db.session.add(new_answer)
        
        user.completion_time = round(time.time() - session['start_time'])

        try:
            db.session.commit()
            return redirect(url_for('quiz_bp.thank_you', username=username))
        except Exception as e:
            db.session.rollback()
            return f"An error occurred while saving your answers: {str(e)}", 500

    return render_template('quiz.html', questions=QUESTIONS)

@quiz_bp.route('/scoreboard')
def scoreboard():
    users = User.query.order_by(User.score.desc(), User.completion_time.asc()).all()    
    return render_template('scoreboard.html', users=users)