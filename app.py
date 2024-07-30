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
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.Column(db.JSON) 

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
    if user_id is None:
        return redirect('/')
    
    if request.method == 'GET':
        with open('data/questions.json') as file:
            questions = json.load(file)
        selected_questions = random.sample(questions, 10)
        session['questions'] = selected_questions
        return render_template('test.html', user_id=user_id, questions=selected_questions)
    
    elif request.method == 'POST':
        selected_questions = session.get('questions', [])
        answers_dict = {f'answer_{question["id"]}': request.form.get(f'answer_{question["id"]}') for question in selected_questions}
        
        new_answer = Answer(user_id=user_id, answers=answers_dict)
        try:
            db.session.add(new_answer)
            db.session.commit()
            return redirect('/score')
        except Exception as e:
            return f'There was an issue: {str(e)}'

    return render_template('test.html', user_id=user_id)

@app.route('/score')
def score_page():
    return render_template('score.html')

if __name__ == '__main__':
    app.run(debug=True)