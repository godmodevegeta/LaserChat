import json
from typing import Optional

def load_temp_db() -> list[dict]:
    with open('users.json') as f:
        users = json.load(f)
    return users

def write_temp_db(users: list) -> None:
    with open('users.json', 'w') as f:
        json.dump(users, f)

def validate_signup_body(data: Optional[dict]) -> list[bool, str]:
    # if not all(key in data for key in ['username', 'password', 'email']):
    #     return jsonify({'error': 'Missing required fields'}), 400
    for key in ['email', 'username', 'password']:
        if key not in list(data.keys()):
            return [False, key]
    return [True]

def check_if_user_already_exists(users: list[dict], data: dict) -> list[bool, str]:
    for user in users:
        if user.get('username') == data.get('username'):
            return [False, 'Username']
        if user.get('email') == data.get('email'):
            return [False, 'Email']
    return [True]



        