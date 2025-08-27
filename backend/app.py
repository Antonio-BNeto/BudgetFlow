import os
from flask import Flask
from db.db import db
from routes import register_routes

app = Flask(__name__)  # Inicia a aplicação Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budgetflow.db'  # Configuração do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Inicializa o banco de dados com a aplicação

register_routes(app)  # Registra as rotas

if __name__ == "__main__":
    
    os.makedirs('instance', exist_ok=True)  # Garante que a pasta instance exista
    
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
