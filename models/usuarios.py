from flask_login import UserMixin
from ..db import database

class Usuario(database.Model, UserMixin):
    __tablename__ = "usuarios"

    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(100), unique=True, nullable=False)
    senha = database.Column(database.String(255), nullable=False)

    buracos = database.relationship('Buraco', backref='autor', lazy=True)

    def __repr__(self):
        return f'<{self.nome}>'