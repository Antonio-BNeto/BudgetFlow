from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum # Importa do SQLAlchemy os tipos e funções necessários para definir colunas de tabelas no banco de dados:
from sqlalchemy.orm import relationship # Definir um relacionamento entre tabelas
from db.db import Base  # Base declarativa do SQLAlchemy
import enum # módulo do Python para criar tipos enumeradores

class Category(Base): # Define a tabela de categorias

    __tablename__ = 'categories'  # Nome da tabela no banco de dados
    
    category_id = Column(Integer, primary_key=True, index=True)  # Coluna de ID, chave primária e indexada
    name = Column(String, unique=True, nullable=False)  # Coluna de nome da categoria, não pode ser nula e não repete

    transactions = relationship("Transaction", back_populates="category")  # Relacionamento com a tabela de transações
    budgets = relationship("Budget", back_populates="category")  # Relacionamento com a tabela de orçamentos
 
class TransactionType(enum.Enum): # Define um tipo enumerador para os tipos de transações
    income = "income" # Receita
    expense = "expense" # Despesa

class Transaction(Base): # Define a tabela de transações

    __tablename__ = 'transactions'  # Nome da tabela no banco de dados
    
    transaction_id = Column(Integer, primary_key=True, index=True)  # Coluna de ID da transação, chave primária e indexada
    type = Column(Enum(TransactionType), nullable=False)  # Coluna de tipo da transação, não pode ser nula
    amount = Column(Float, nullable=False)  # Coluna de valor da transação, não pode ser nula
    date = Column(Date, nullable=False)  # Coluna de data da transação, não pode ser nula
    description = Column(String, nullable=True)  # Coluna de descrição da transação, pode ser nula
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)  # Chave estrangeira para a categoria, não pode ser nula

    category = relationship("Category", back_populates="transactions") # Relacionamento com a tabela de categorias

class Budget(Base): # Define a tabela de orçamentos

    __tablename__ = 'budgets' # Nome da tabela no banco de dados

    budget_id = Column(Integer, primary_key=True, index=True)  # Coluna de ID do orçamento, chave primária e indexada
    month = Column(String, nullable=False)  # Coluna de mês do orçamento, não pode ser nula
    limit = Column(Float, nullable=False)  # Coluna de limite do orçamento, não pode ser nula
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)  # Chave estrangeira para a categoria, não pode ser nula

    category = relationship("Category", back_populates="budgets")  # Relacionamento com a tabela de categorias