from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import inspect

# refers to self
app = Flask(__name__)
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# define database
class User(db.Model):
    #initial form
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure this is unique
    age = db.Column(db.Integer)
    gender = db.Column(db.String(80))
    def __repr__(self):
        return '<User %r>' % self.id
    
class Answer(db.Model):
    #initial form
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure this is unique
    answer = db.Column(db.String(300))
    def __repr__(self):
        return '<Answer %r>' % self.id

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
        user_id = request.form.get('id')  # Hidden field for user ID
        answer = request.form.get('answer_1', 'answer_2', 'answer_3', 'answer_4')     # Form field for age
    
    return render_template('test.html')

if __name__ == '__main__':
    app.run(debug=True)