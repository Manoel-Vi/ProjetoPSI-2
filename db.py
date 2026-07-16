from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)

def criar_tabela():
    class Usuario(db.Model):
        __tablename__ = "usuarios"

        id = db.Column(db.Integer, primary_key=True)
        nome = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        senha = db.Column(db.String(255), nullable=False)


        def __repr__(self):
            return f'<{self.nome}>'
        
    with app.app_context():
        db.create_all()