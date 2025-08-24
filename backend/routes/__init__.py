from flask import Flask
from .categories import categories_bp
from .budgets import budgets_bp
from.transactions import transactions_bp

# registra todas as rotas
def register_routes(app: Flask):
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(budgets_bp, url_prefix="/api/budgets")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")