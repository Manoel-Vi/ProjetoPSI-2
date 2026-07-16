from flask import Flask, render_template, request, redirect, url_for
from models import Usuario, Buraco
from db import database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.init_app(app)

with app.app_context():
    database.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        database.session.add(novo_usuario)
        database.session.commit()

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

@app.route('/logout')
def logout():
    return redirect(url_for('index'))