from flask import Flask
from routes import register_routes

app = Flask(__name__)  # Inicia a aplicação Flask
register_routes(app)  # Registra as rotas

if __name__ == "__main__":
    app.run(debug=True)
