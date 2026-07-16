from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Usuario(database.Model):
        __tablename__ = "usuarios"

        id = database.Column(database.Integer, primary_key=True)
        nome = database.Column(database.String(100), nullable=False)
        email = database.Column(database.String(100), unique=True, nullable=False)
        senha = database.Column(database.String(255), nullable=False)


        def __repr__(self):
            return f'<{self.nome}>'