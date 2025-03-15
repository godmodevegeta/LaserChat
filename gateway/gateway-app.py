from flask import Flask, request, jsonify
import requests
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")

AUTH_SERVICE_URL = config.get('AUTH_SERVICE_URL')
CHAT_SERVICE_URL = config.get('CHAT_SERVICE_URL')

@app.before_request
def authenticate_request():
    """ Intercepts all requests and validates JWT """
    if request.path.startswith("/api/v1/message"):  # Protect only /message
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        token = token.split(" ")[1] # Remove Bearer
        validation_response = validate_jwt(token)
        if not validation_response:
            return jsonify({'message': 'Invalid or expired token'}), 401
        request.user = validation_response.json()


@app.route('/api/v1/message', methods=['POST'])
def message():
    """ Forwards request to the CHAT Microservice """
    headers = {"Authorization": request.headers.get("Authorization")}
    response = requests.post(f"{CHAT_SERVICE_URL}/api/v1/message", headers=headers)
    return jsonify(response.json()), response.status_code
    

def validate_jwt(token: str):
    """SENDS jwt to AUTH service for validation"""
    response = requests.post(
        f'{AUTH_SERVICE_URL}/validate', 
        data={
            'token': token
            }
        )
    return response if response.status_code==200 else None


if __name__=='__main__':
    app.run(debug=True, port=8003)