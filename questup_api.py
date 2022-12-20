from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def init():
    pass


app.run(host="0.0.0.0", port=6001)