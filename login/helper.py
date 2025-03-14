import json
from typing import Optional
import hashlib
import datetime
import jwt
from dotenv import dotenv_values

# Load Environment Variables
config = dotenv_values('.env')
SECRET_JWT_KEY = config.get('SECRET_JWT_KEY')
SECRET_JWT_ALGORITHM = config.get('SECRET_JWT_ALGORITHM')

def load_temp_db() -> list[dict]:
    with open('users.json') as f:
        users = json.load(f)
    return users

def write_temp_db(users: list) -> None:
    with open('users.json', 'w') as f:
        json.dump(users, f)

def add_new_user(users: list[dict], user: dict) -> list[dict]:
    # Create new user
    new_user = {
            'email': user['email'],
            'username': user['username'],
            'password': hash_password(user['password'])
        }
    # Add user
    users.append(new_user)
    return users
    

def validate_signup_body(data: Optional[dict]) -> list[bool, str]:
    # if not all(key in data for key in ['username', 'password', 'email']):
    #     return jsonify({'error': 'Missing required fields'}), 400
    for key in ['email', 'username', 'password']:
        if key not in list(data.keys()):
            return [False, key]
    return [True]

def check_if_user_already_exists(users: list[dict], data: dict) -> list[bool, str, str]:
    for user in users:
        if user.get('username') == data.get('username'):
            return [True, 'Username', data.get('username')]
        if user.get('email') == data.get('email'):
            return [True, 'Email', data.get('email')]
    return [False]

def validate_login_body(data: dict) -> list[bool, str]:
    for key in ['username', 'password']:
        if key not in list(data.keys()):
            return [False, key]
    return [True]

def check_user_password(data: dict) -> bool:
    request_username = data.get('username')
    request_password = hash_password(data.get('password'))
    users = load_temp_db()
    for user in users:
        if user.get('username') == request_username:
            return user.get('password') == request_password
        
def hash_password(password: str) -> str:
    # Create a sha256 hash object from the password
    hash_object = hashlib.sha256(password.encode())
    # Convert the hash to a hexadecimal string and return it
    return hash_object.hexdigest()    

def generate_jwt_token(username: str) -> str:
    token = jwt.encode(
        {
            'username': username,
            'expiry': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat()
        }, 
        SECRET_JWT_KEY, 
        algorithm=SECRET_JWT_ALGORITHM
    )
    return token
