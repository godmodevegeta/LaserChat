from flask import jsonify

def get_user_from_jwt(headers):
    token = headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401
    token = token.split(" ")[1] # Remove Bearer

