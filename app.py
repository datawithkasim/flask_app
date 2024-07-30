from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import inspect
import random
import json
import os 

app = Flask(__name__) # create the Flask app
app.secret_key = 'your_secret_key' # shitty secret key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # connect to the database
db = SQLAlchemy(app) # initialize the database

class User(db.Model): # Define User table
    __tablename__ = 'user'  # Explicitly set the table name

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(80))

    def __repr__(self):
        return f'<User {self.id}>'

# Define Answer table
class Answer(db.Model):
    __tablename__ = 'answer'  # Explicitly set the table name

    # Define columns
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_1 = db.Column(db.String(50))
    answer_2 = db.Column(db.String(50))
    answer_3 = db.Column(db.String(50))
    answer_4 = db.Column(db.String(50))
    answer_5 = db.Column(db.String(50))
    answer_6 = db.Column(db.String(50))
    answer_7 = db.Column(db.String(50))
    answer_8 = db.Column(db.String(50))
    answer_9 = db.Column(db.String(50))
    answer_10 = db.Column(db.String(50))

    def __repr__(self):
        return f'<Answer {self.id}>'

#route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Retrieve form data
        user_id = request.form.get('id')  # Hidden field for user ID
        age = request.form.get('age')     # Form field for age
        gender = request.form.get('gender')  # Form field for gender

        # Convert and validate data
        try:
            # Convert `age` to integer
            age = int(age)

            # `user_id` might be None or an integer; ensure it’s handled correctly
            user_id = int(user_id) if user_id else None

            # Gender should be a valid string; check constraints if needed
            if gender not in ['male', 'female']:
                raise ValueError("Invalid gender value.")
        except (ValueError, TypeError) as e:
            return f"Invalid input: {str(e)}"

        # Create a new User instance
        user_stats = User(id=user_id, age=age, gender=gender)

        try:
            db.session.add(user_stats)
            db.session.commit()

            # Set user_id in session
            session['user_id'] = user_stats.id

            return redirect('/test')
        except Exception as e:
            return f'There was an issue: {str(e)}'
        
    return render_template('index.html')

@app.route('/test', methods=['POST', 'GET'])
def test_page():
    user_id = session.get('user_id')

    # Check if the user_id exists in the session
    if user_id is None:
        # If not, redirect to the index to likely prompt login or session start
        return redirect('/')

    if request.method == 'GET':
        # Load questions from JSON file
        with open('data/questions.json') as file:
            questions = json.load(file)

        # Randomly select 10 questions
        selected_questions = random.sample(questions, 10)

        # Render these questions on the test page
        return render_template('test.html', user_id=user_id, questions=selected_questions)

    elif request.method == 'POST':
        # Retrieve form data and handle the submission
        answers = {
            'user_id': user_id,
            'answer_1': request.form.get(f'answer_{{q.id}}'),
            'answer_2': request.form.get(f'answer_{{q.id}}'),
            'answer_3': request.form.get(f'answer_{{q.id}}'),
            'answer_4': request.form.get(f'answer_{{q.id}}'),
            'answer_5': request.form.get(f'answer_{{q.id}}'),
            'answer_6': request.form.get(f'answer_{{q.id}}'),
            'answer_7': request.form.get(f'answer_{{q.id}}'),
            'answer_8': request.form.get(f'answer_{{q.id}}'),
            'answer_9': request.form.get(f'answer_{{q.id}}'),
            'answer_10': request.form.get(f'answer_{{q.id}}')
        }

        # Create a new Answer instance
        new_answer = Answer(**answers)

        try:
            db.session.add(new_answer)
            db.session.commit()

            return redirect('/score')
        except Exception as e:
            return f'There was an issue: {str(e)}'

    # Handle other methods if necessary
    return render_template('test.html', user_id=user_id)

@app.route('/score')
def score_page():
    return render_template('score.html')

if __name__ == '__main__':
    app.run(debug=True)