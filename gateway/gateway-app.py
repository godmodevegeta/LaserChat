from flask import Flask

app = Flask(__name__)

@app.route('/api/v1/message', methods=['POST'])
def message():
    pass