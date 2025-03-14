from flask import Flask, request, jsonify, redirect, url_for
import json
# from model import LoginBody
import helper

app = Flask(__name__)

@app.route("/")
def hello_login():
    return "<p>Hello, Login!</p>"

# login api
# - Define a route for login (e.g., /login)
# - Accept POST requests with user credentials (username and password)
# - Validate the credentials
# - Return a success message or an error message
@app.route("/api/v1/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({'message': 'This is a GET request. Please use POST and send appropriate body to login'}), 405
    elif request.method == 'POST':
        data = request.get_json()
        users = helper.load_temp_db()

        # Validate login body
        valid_body = helper.validate_login_body(data)
        if not valid_body[0]: return jsonify({'error': f'Missing field {valid_body[1]} in body'}), 400

        # Check if username exists
        user_exists = helper.check_if_user_already_exists(users, data)
        if user_exists[0]: # if username already exists
            username = user_exists[2]
            user_password_check = helper.check_user_password(data)
            if user_password_check: 
                token = helper.generate_jwt_token(username)
                return jsonify({'message': f'User {username} logged in successfully', 'token': token}), 200
            return jsonify({'error': 'Incorrect password. Please try again.'}), 401
        else: # if username doesn't exist
            return jsonify({'error': 'Username does not exist'}), 400

# signup api
# - Define a route for signup (e.g., /signup)
# - Accept POST requests with user details (username, password, email, etc.)
# - Validate the input data
# - Create a new user in the database
# - Return a success message or an error message
@app.route("/api/v1/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return jsonify({'message': 'This is a GET request. Please use POST and send appropriate body to signup'}), 405
    elif request.method == 'POST':
        users = helper.load_temp_db()
        data = request.get_json()
        
        # Validate required fields
        valid_body = helper.validate_signup_body(data)
        if not valid_body[0]: return jsonify({'error': f'Missing field {valid_body[1]} in body'}), 400
        
        # Check if username or email already exists
        user_exists = helper.check_if_user_already_exists(users, data)
        if user_exists[0]: return jsonify({'error': f'{user_exists[1]} [{user_exists[2]}] already exists'}), 400

        # Add new user to users
        users = helper.add_new_user(users, data)

        # Persist user in file
        helper.write_temp_db(users)

        return jsonify({'message': 'User created successfully'}), 201

# logout api
# - Define a route for logout (e.g., /logout)
# - Handle user session termination
# - Return a success message
@app.route("/api/v1/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return 'hi, GET'
    elif request.method == 'POST':
        return 'hi, POST'


if __name__ == "__main__":
    app.run(debug=True, port=8001)


