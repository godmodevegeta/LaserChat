from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_login():
    return "<p>Hello, Login!</p>"

# login api

# signup api

# logout api

if __name__ == "__main__":
    app.run(debug=True, port=8001)

