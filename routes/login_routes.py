import json

import firebase_admin
import pyrebase as pb
from firebase_admin import credentials, auth
from flask import request, render_template, session
from google.auth.transport import requests

from endpoints_configs import FIREBASE_ADMIN_CONFIG, PYREBASE_CONFIG
from main_app import app

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_ADMIN_CONFIG)
firebase = firebase_admin.initialize_app(cred)
firebase_request_adapter = requests.Request()

# Initialise pyrebase handler
firebase_pb_handler = pb.initialize_app(json.load(open(PYREBASE_CONFIG)))


@app.route('/signup', methods=['POST'])
def signup():
    # If the user submitted the login form
    if request.method == 'POST':

        # Get the username and password from the form
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            print('user created')
            user = auth.create_user(email=email, password=password)
        except Exception as e:
            return str(e)

        # Sign in the user
        try:
            firebase_id_token = auth.create_custom_token(user.uid)
            if firebase_id_token:
                session['firebase_id_token'] = firebase_id_token
        except Exception as e:
            # Handle errors
            return str(e)

    return render_template('home/index.html', segment='index')


@app.route('/login', methods=['POST'])
def login():
    # Get the user's email and password from the request body

    if 'firebase_id_token' in session:
        return render_template('home/index.html', segment='index')

    if request.method == 'POST':

        # login with email and password
        email = request.form.get('email')
        password = request.form.get('password')

        # Sign in the user with email and password
        try:
            user = firebase_pb_handler.auth().sign_in_with_email_and_password(email, password)
            firebase_id_token = user['idToken']
            session['firebase_id_token'] = firebase_id_token
            return render_template('home/index.html', segment='index')

        except Exception as e:
            # Handle errors
            return str(e)
    else:
        return '''
            <form method="post">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <input type="submit" value="Login">
            </form>
        '''

    # db = firebase_pb_handler.database()
    #
    # # data to save
    # data = {
    #     "name": "Mortimer 'Morty' Smith"
    # }
    #
    # # Pass the user's idToken to the push method
    # results = db.child("users").push(data, user['idToken'])
    #
    # claims = google.oauth2.id_token.verify_firebase_token(
    #     token, firebase_request_adapter)
