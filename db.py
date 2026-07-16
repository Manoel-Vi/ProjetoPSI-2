from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy(app)

def criar_tabela():
        
    with app.app_context():
        db.create_all()