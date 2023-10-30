from flask import Flask
from Scrape import get_pis
app = Flask(__name__)

@app.route('/')
def hello_world():
    get_pis()
    return 'Hello, World!'