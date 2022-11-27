from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os,re,io
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'abc123'

# Enter your database connection details below
#Change before using
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jan2021!'
app.config['MYSQL_DB'] = 'sync'
mysql = MySQL(app)

# configuration of mail
'''
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adityaa.ramachandran@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
'''
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''  # Output message
    if request.method == 'POST' and 'Name' in request.form and 'Roll Number' in request.form:
        # Create variables for easy access
        name = request.form['Name']
        roll = request.form['Roll Number']
        event = request.form['Event']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE name = %s AND roll = %s', (name, roll,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            cursor.execute(
                'INSERT INTO eventreg VALUES (NULL, %s, %s, %s)', (name, roll, event,))
            mysql.connection.commit()
            msg = f'You have successfully registered for {event}!'
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST' and 'Name' in request.form and 'Roll Number' in request.form and 'Contact' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['Name']
        roll = request.form['Roll Number']
        contact = request.form['Contact']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE roll = %s OR email = %s', (roll, email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[0-9]+',contact):
            msg = 'Contact must contact only numbers!'
        elif not roll or not contact or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (name, roll, contact, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            '''
            msg1 = Message(
                'Confirmation Mail - Sync Events Registration',
                sender='adityaa.ramachandran@gmail.com',
                recipients=[email]
            )
            msg1.body = 'This mail is to inform you that you have successfully registered for SYNC\'22\n\nName: ' + \
                name + '\nRoll Number: ' + roll + '\n\n' + 'Regards,\nEvents team, CSEA'
            mail.send(msg1)
            '''

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
