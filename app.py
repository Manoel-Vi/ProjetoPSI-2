from flask import Flask, render_template, render_template_string, request, redirect, url_for, abort, flash
from .models import Usuario, Buraco
from flask_login import current_user, logout_user, login_user, LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .db import database


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'ROMERITO_CORREDOR'

database.init_app(app)


with app.app_context():
    database.create_all()

@login_manager.user_loader
def load_user(user_id):
    return database.session.get(Usuario, int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        senha_hash = generate_password_hash(senha)
        
        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.')
            return redirect(url_for('cadastro'))

        usuario_ja_existe = Usuario.query.filter_by(email=email).first()
        if usuario_ja_existe:
            abort(400)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
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

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for("home"))
        
        else:
            flash('E-mail ou senha incorretos. Tente novamente!')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(400)
def erro400(error):
    return render_template('erros/erro400.html'), 400

@app.route("/cadastrar-buraco", methods=["GET","POST"])
@login_required
def cadastrar_buraco():

    if request.method == "POST":
        rua = request.form["rua"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        gravidade = request.form["gravidade"]

        novo_buraco = Buraco(
            rua=rua,
            bairro=bairro,
            cidade=cidade,
            gravidade=gravidade,
            usuario_id=current_user.id
        )

        database.session.add(novo_buraco)
        database.session.commit()

        return redirect(url_for("listar_buracos"))

    return render_template('cadastro_buraco.html')

@app.route("/listar-buracos")
@login_required
def listar_buracos():
    buracos = Buraco.query.all()
    return render_template("listar_buracos.html", buracos=buracos)

@app.route("/apagar-buraco/<int:id>")
@login_required
def apagar_buraco(id):
    buraco = Buraco.query.get_or_404(id)
    database.session.delete(buraco)
    database.session.commit()
    return redirect(url_for("listar_buracos"))

@app.route("/editar-buraco/<int:id>", methods=["GET", "POST"])
@login_required
def editar_buraco(id):
    buraco = Buraco.query.get_or_404(id)
    if request.method == "POST":
        buraco.rua = request.form["rua"]
        buraco.bairro = request.form["bairro"]
        buraco.cidade = request.form["cidade"]
        buraco.gravidade = request.form["gravidade"]
        database.session.commit()

        return redirect(url_for("listar_buracos"))
    return render_template("editar_buraco.html", buraco=buraco)