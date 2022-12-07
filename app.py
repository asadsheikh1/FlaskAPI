from flask import Flask


app = Flask(__name__)

@app.route('/')
def welcome():
    return "Welcome to Course Mania."

from controller import *


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
