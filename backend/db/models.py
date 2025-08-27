from flask_sqlalchemy import SQLAlchemy
import enum

from db.db import db  # Importa a instância do SQLAlchemy

# -----------------------------------------------------------------------------
# Enum para o tipo de transação
# -----------------------------------------------------------------------------
class TransactionType(enum.Enum): # Define um tipo enumerador para os tipos de transações
    income = "income" # Receita
    expense = "expense" # Despesa

# -----------------------------------------------------------------------------
# Modelo de Categoria
# -----------------------------------------------------------------------------
class Category(db.Model): # Define a tabela de categorias

    __tablename__ = 'categories'  # Nome da tabela no banco de dados

    category_id = db.Column(db.Integer, primary_key=True, index=True)  # Coluna de ID, chave primária e indexada
    name = db.Column(db.String, unique=True, nullable=False)  # Coluna de nome da categoria, não pode ser nula e não repete

    transactions = db.relationship("Transaction", back_populates="category")  # Relacionamento com a tabela de transações
    budgets = db.relationship("Budget", back_populates="category")  # Relacionamento com a tabela de orçamentos

# -----------------------------------------------------------------------------
# Modelo de Transação
# -----------------------------------------------------------------------------
class Transaction(db.Model): # Define a tabela de transações

    __tablename__ = 'transactions'  # Nome da tabela no banco de dados

    transaction_id = db.Column(db.Integer, primary_key=True, index=True)  # Coluna de ID da transação, chave primária e indexada
    type = db.Column(db.Enum(TransactionType), nullable=False)  # Coluna de tipo da transação, não pode ser nula
    amount = db.Column(db.Float, nullable=False)  # Coluna de valor da transação, não pode ser nula
    date = db.Column(db.Date, nullable=False)  # Coluna de data da transação, não pode ser nula
    description = db.Column(db.String, nullable=True)  # Coluna de descrição da transação, pode ser nula
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)  # Chave estrangeira para a categoria, não pode ser nula

    category = db.relationship("Category", back_populates="transactions") # Relacionamento com a tabela de categorias

# -----------------------------------------------------------------------------
# Modelo de Orçamento
# -----------------------------------------------------------------------------
class Budget(db.Model): # Define a tabela de orçamentos

    __tablename__ = 'budgets' # Nome da tabela no banco de dados

    budget_id = db.Column(db.Integer, primary_key=True, index=True)  # Coluna de ID do orçamento, chave primária e indexada
    month = db.Column(db.Date, nullable=False)  # Coluna de mês do orçamento, não pode ser nula
    limit = db.Column(db.Float, nullable=False)  # Coluna de limite do orçamento, não pode ser nula
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)  # Chave estrangeira para a categoria, não pode ser nula

    category = db.relationship("Category", back_populates="budgets")  # Relacionamento com a tabela de categorias