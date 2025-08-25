from flask import Blueprint, request, jsonify 
from db.db import session_scope 
from db.models import Transaction

# Criando o blueprint para transações (conjunto de rotas do recurso Transaction)
transactions_bp = Blueprint('transactions', __name__)

# -----------------------------
# GET /api/transactions → listar todas as transações
# -----------------------------
@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    with session_scope() as db:
        transactions = db.query(Transaction).all()
        return jsonify([{"transaction_id": t.transaction_id, "amount": t.amount, "category_id": t.category_id} for t in transactions])

# -----------------------------
# POST /api/transactions → criar uma nova transação
# -----------------------------
@transactions_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.json
    with session_scope() as db:
        new_transaction = Transaction(**data) # desestruturando o dicionário
        db.add(new_transaction)
        return jsonify({"transaction_id": new_transaction.transaction_id, "amount": new_transaction.amount, "category_id": new_transaction.category_id}), 201

# -----------------------------
# PUT /api/transactions/<int:transaction_id> → Atualizar uma transação existente
# -----------------------------
@transactions_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.json
    with session_scope() as db:
        transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        
        for key, value in data.items():
            setattr(transaction, key, value)

        db.flush()
        
        return  jsonify(
            {
                "transaction_id": transaction.transaction_id,
                "amount": transaction.amount,
                "category_id": transaction.category_id
            }
        )

# -----------------------------
# DELETE /api/transactions/<int:transaction_id> → Deletar uma transação existente
# -----------------------------
@transactions_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    with session_scope() as db:
        transaction = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        db.delete(transaction)
        db.flush()

        return jsonify({"message": "Transaction deleted successfully"}), 204