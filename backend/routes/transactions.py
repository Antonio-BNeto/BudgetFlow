from flask import Blueprint, request, jsonify 
from db.db import session_scope 
from db.models import Transaction
from schemas.transactions import TransactionCreate, TransactionResponse
from datetime import date

# Criando o blueprint para transações (conjunto de rotas do recurso Transaction)
transactions_bp = Blueprint('transactions', __name__)

# -----------------------------
# GET /api/transactions → listar todas as transações
# -----------------------------
@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    with session_scope() as session:
        transactions = session.query(Transaction).all()
        response = [
            TransactionResponse.model_validate(t).model_dump()
            for t in transactions
        ]
        return jsonify(response), 200

# -----------------------------
# POST /api/transactions → criar uma nova transação
# -----------------------------
@transactions_bp.route('/transactions', methods=['POST'])
def create_transaction():
    try:
        transaction_data = TransactionCreate(**request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    with session_scope() as session:

        new_transaction = Transaction(
            type=transaction_data.type,
            amount=transaction_data.amount,
            date=transaction_data.date,
            description=transaction_data.description,
            category_id=transaction_data.category_id
        ) 
        
        session.add(new_transaction)
        session.flush()  # Para garantir que o ID seja gerado
        session.refresh(new_transaction)

        response = TransactionResponse.model_validate(new_transaction).model_dump()
        return jsonify(response), 201

# -----------------------------
# PUT /api/transactions/<int:transaction_id> → Atualizar uma transação existente
# -----------------------------
@transactions_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    
    try:
        transaction_data = TransactionCreate(**request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    with session_scope() as session:
        transaction = (
            session.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )

        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        

        transaction.type = transaction_data.type
        transaction.amount = transaction_data.amount
        transaction.date = transaction_data.date
        transaction.description = transaction_data.description
        transaction.category_id = transaction_data.category_id

        session.flush()
        session.refresh(transaction)

        response = TransactionResponse.model_validate(transaction).model_dump()
        return jsonify(response), 200

# -----------------------------
# DELETE /api/transactions/<int:transaction_id> → Deletar uma transação existente
# -----------------------------
@transactions_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    with session_scope() as session:
        transaction = (
            session.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )
        
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        session.delete(transaction)
        session.flush()

        return jsonify({"message": "Transaction deleted successfully"}), 204