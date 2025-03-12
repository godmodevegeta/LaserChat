from flask import Flask, request

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
        return 'hi, GET'
    elif request.method == 'POST':
        return 'hi, POST'


# signup api
# - Define a route for signup (e.g., /signup)
# - Accept POST requests with user details (username, password, email, etc.)
# - Validate the input data
# - Create a new user in the database
# - Return a success message or an error message
@app.route("/api/v1/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return 'hi, GET'
    elif request.method == 'POST':
        return 'hi, POST'

    

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


