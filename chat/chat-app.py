from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_chat():
    return "<p>Hello, Chat!</p>"


@app.route("/api/v1/message", methods=['POST'])
def hello_message():
    return jsonify({
        'message': "Welcome to CHAT!!!!"
    })


if __name__ == "__main__":
    app.run(debug=True, port=8002)