from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

AUTH_SERVICE_URL = config.get('AUTH_SERVICE_URL')
AUTH_VALIDATION_PATH = config.get('AUTH_VALIDATION_PATH')
CHAT_SERVICE_URL = config.get('CHAT_SERVICE_URL')
CHAT_MESSAGE_PATH = config.get('CHAT_MESSAGE_PATH')


def validate_jwt(token: str):
    """SENDS jwt to AUTH service for validation"""
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f'{AUTH_SERVICE_URL}{AUTH_VALIDATION_PATH}', 
        headers=headers,
        json={
            'token': token
            }
        )
    
    return response if response.status_code==200 else None


def create_response(headers):
    return requests.post(f"{CHAT_SERVICE_URL}{CHAT_MESSAGE_PATH}", headers=headers)