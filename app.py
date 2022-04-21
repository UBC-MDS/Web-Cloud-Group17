from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, MDS world!"

@app.route("/fashion")
def fashion():
    return "I think you'd look great in a bow tie."