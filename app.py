from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import inspect

# refers to self
app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define User table
class User(db.Model):
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
            return redirect('/test')
        except Exception as e:
            return f'There was an issue: {str(e)}'
        
    return render_template('index.html')

@app.route('/test', methods=['POST', 'GET'])
def test_page():
    if request.method == 'POST':
        # Handle the POST request here
        # Retrieve form data
        id = request.form.get('id')
        user_id = request.form.get('user_id')  # Hidden field for user ID
        answer_1 = request.form.get('answer_1')
        answer_2 = request.form.get('answer_2')
        answer_3 = request.form.get('answer_3')
        answer_4 = request.form.get('answer_4')
        answer_5 = request.form.get('answer_5')
        answer_6 = request.form.get('answer_6')
        answer_7 = request.form.get('answer_7')
        answer_8 = request.form.get('answer_8')
        answer_9 = request.form.get('answer_9')
        answer_10 = request.form.get('answer_10')

        try:
            # Create a new Answer instance
            new_answer = Answer(
                user_id=user_id,
                answer_1=answer_1,
                answer_2=answer_2,
                answer_3=answer_3,
                answer_4=answer_4,
                answer_5=answer_5,
                answer_6=answer_6,
                answer_7=answer_7,
                answer_8=answer_8,
                answer_9=answer_9,
                answer_10=answer_10
            )

            # Add and commit the new_answer instance to the database session
            db.session.add(new_answer)
            db.session.commit()
            return redirect('/score')
        except Exception as e:
            return f'There was an issue: {str(e)}'

    return render_template('test.html')

@app.route('/score')
def score_page():
    return render_template('score.html')

if __name__ == '__main__':
    app.run(debug=True)