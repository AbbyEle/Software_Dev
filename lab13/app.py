"""
Abigail Elena
lab 13, Flask application
"""
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Create an object 'app' from the Flask module
app = Flask(__name__)

# Connecting to PostgreSQL - ensure password is URL-encoded if it includes special characters like @
# Replace 'username', 'password', 'localhost', and 'dbname' with actual values
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:AEKAkosua91Elena@@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a db object
db = SQLAlchemy(app)

# create a secret key to handle data within our server
import os
app.config[]

# Define a model (creates a table in the connected database)
class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 'Successfully requested! Entered password = ' + request.form['password']
    name = "Abig"
    checkfruit = "pineapple"
    fruits = ['apple', 'orange', 'grapes']
    return render_template('index.html', username=name, listfruits=fruits, checkfruit=checkfruit)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/users', methods =['GET', 'POST'])
def users():
    if request.method == 'POST':
        try:
            form = request.form
            emp_name = form['employee_name']
            emp_id = form['employee_id']

            # check if the employee already exists by name (or use employee_id if that's unique)
            existing_employee = Employee.query.filter_by(employee_name=emp_name).first() #boolean (True, False)
            existing_id = Employee.query.filter_by(employee_id = emp_id) .first() #boolean (True, False)

            if existing_employee:
                return(f"Employee with name '{emp_name}' already exists!")
            if existing_id:
                return(f"Employee with id '{emp_id}' already exists!")

 # create a new employee object and add form data into the database
    new_employee = Employee(employee_id = emp_id, employee_name = emp_name)

# store new employee name in session
session['employee1'] = new_employee.employee_name
employee_name

#add the new object to our database
db.session.add(new_employee)
db.session.commit()

# message using flash
flash(f"{request.form['employee_name']} successfully added!")
except:
    flash("Fail to insert data! Try again")
return render_template('users.html')


@app.route('/quotes')
def quotes():
    return redirect(url_for('index'))

# Set the 'app' to run if this file is executed directly (not when imported)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

   







