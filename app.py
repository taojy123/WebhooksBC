# coding: utf-8


from flask import Flask


app = Flask(__name__)



@app.route('/')
def index():
    return 'Hello world'


@app.route('/wehbooks/')
def wehbooks():
    return 'Hello webhooks'


