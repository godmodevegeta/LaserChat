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
    


@app.route('/api/v1/message', methods=['POST'])
def message():
    pass

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