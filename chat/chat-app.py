from flask import Flask, jsonify, request
import helper
import logging

app = Flask(__name__)

logger = logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

@app.route("/")
def hello_chat():
    return "<p>Hello, Chat!</p>"


@app.route("/api/v1/message", methods=['POST'])
def hello_message():
    userID = request.headers.get('UserID')
    return jsonify({
        'message': f"Welcome to CHAT, {userID}!!!!"
    })


if __name__ == "__main__":
    app.run(debug=True, port=8002)