from flask import Flask, request, jsonify
import requests
import helper
import logging

app = Flask(__name__)

logger = logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

@app.before_request
def authenticate_request():
    """ Intercepts all requests and validates JWT """
    if request.path.startswith("/api/v1/message"):  # Protect only /message
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        token = token.split(" ")[1] # Remove Bearer
        validation_response = helper.validate_jwt(token)
        if not validation_response:
            return jsonify({'message': 'Invalid or expired token'}), 401
        request.user = validation_response.json()


@app.route('/api/v1/message', methods=['POST'])
def message():
    """ Forwards request to the CHAT Microservice """
    print("______Preparing to contact CHAT______")
    userId = request.user.get('user')
    headers = {
        "Authorization": request.headers.get("Authorization"),
        "UserID": userId
        }
    response = helper.create_response(headers)
    return response.json(), response.status_code
    


if __name__=='__main__':
    app.run(debug=True, port=8003)