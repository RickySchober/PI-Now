from flask import Flask
from Scrape import scrape

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/deez')
def deez():
    scrape()
    return "deez"