from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_temlate('cadastro.html')

@app.route('/login')
def login():
    return render_temlate('login.html')