from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.criar_tabela()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logut')
def logout():
    return redirect(url_for('index'))