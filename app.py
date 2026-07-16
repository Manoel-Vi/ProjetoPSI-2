from flask import Flask, render_template, request, redirect, url_for, abort, flash
from models import Usuario, Buraco
from db import database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'ROMERITO_CORREDOR'  

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

        usuario_ja_existe = Usuario.query.filter_by(email=email).first()
        if usuario_ja_existe:
            abort(400)

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

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.senha == senha:
            return redirect(url_for('home'))
        
        else:
            flash('E-mail ou senha incorretos. Tente novamente!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.errorhandler(400)
def erro400(error):
    return render_template('erros/erro400.html'), 400