from flask import Flask, request, jsonify
import helper
import jwt
import logging

"""
This module implements a Flask-based API for user authentication including login, signup, 
JWT token validation, and logout functionalities.
Module Endpoints:
    "/"              - A basic endpoint returning a simple HTML greeting.
    "/api/v1/login"  - Accepts POST requests for user login. It:
                        • Validates the JSON request payload.
                        • Checks for the existence of the user.
                        • Verifies the user's password.
                        • Issues a JWT token if authentication is successful.
                        • Returns error messages for GET requests or authentication failures.
    "/api/v1/signup" - Accepts POST requests for new user registration. It:
                        • Validates the required user details in the payload.
                        • Checks for existing username or email conflicts.
                        • Registers the new user and writes the entry to a temporary database.
                        • Returns an appropriate success or error response.
    "/validate"      - Accepts POST requests to validate a JWT token. It:
                        • Expects the token in the JSON body.
                        • Verifies and decodes the token using the provided secret key and algorithm.
                        • Returns the username if the token is valid, or an error message if invalid or expired.
    "/api/v1/logout" - A placeholder API for handling user logout with GET or POST methods.
                        It returns a simple confirmation message based on the request method.
Dependencies:
    - Flask: The web micro-framework to build HTTP endpoints.
    - jwt (PyJWT): To encode and decode JSON Web Tokens.
    - helper: A custom module containing helper functions for:
                • Loading and writing the temporary user database.
                • Validating login and signup request bodies.
                • Generating JWT tokens.
                • Checking user existence and password correctness.
Usage:
    Run this module as the main program to start the Flask server on port 8001 in debug mode:
        python login-app.py
Note:
    Ensure that proper security practices are implemented for production use and that 
    the temporary database is replaced with a persistent data store.
"""

app = Flask(__name__)

logger = logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

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
                return jsonify({'message': f'User [{username}] logged in successfully', 'token': token}), 200
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
    
# validate jwt api
@app.route('/api/v1/validate', methods=['POST'])
def validate_token():
    token = request.get_json().get("token")  # Expecting JSON payload: { "token": "JWT_TOKEN" }

    if not token:
        return jsonify({"message": "Token is missing!"}), 401
    
    try:
        payload = jwt.decode(
            token, 
            helper.SECRET_JWT_KEY, 
            helper.SECRET_JWT_ALGORITHM
        )
        return jsonify({"user": payload.get('username')}), 200  # Return username info
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401
    

# logout api
# - Define a route for logout (e.g., /logout)
# - Handle user session termination
# - Return a success message
@app.route("/api/v1/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        return jsonify({'message': 'User logged out via GET.'}), 200
    elif request.method == 'POST':
        # Optionally, add any logout cleanup logic here
        return jsonify({'message': 'User logged out via POST.'}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8001)


