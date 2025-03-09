from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_chat():
    return "<p>Hello, Chat!</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8002)