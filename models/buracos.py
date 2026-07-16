from db import database

class Buraco(database.Model):
    __tablename__ = "buracos"

    id = database.Column(database.Integer, primary_key=True)
    rua = database.Column(database.String(150), nullable=False)
    bairro = database.Column(database.String(100), nullable=False)
    cidade = database.Column(database.String(100), nullable=False)
    gravidade = database.Column(database.String(20), nullable=False)

    usuario_id = database.Column(
        database.Integer,
        database.ForeignKey("usuarios.id"),
        nullable=False
    )

    def __repr__(self):
        return f'<{self.rua}>'