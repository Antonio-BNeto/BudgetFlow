from flask import Blueprint, request, jsonify
from db.db import session_scope  # Importa o gerenciador de contexto da sessão
from db.models import Budget  # Importa o modelo Budgets
from schemas.budgets import BudgetCreate, BudgetResponse
from datetime import date

# Criando o blueprint para orçamentos (conjunto de rotas do recurso Budget)
budgets_bp = Blueprint('budgets', __name__)

# -----------------------------
# GET /api/budgets → listar todos os orçamentos
# -----------------------------
@budgets_bp.route('/budgets', methods=['GET'])
def get_budgets():
    with session_scope() as session:
        budgets = session.query(Budget).all() # Retorna uma lista com todos os orçamentos

        response = [
            BudgetResponse.model_validate(b).model_dump()
            for b in budgets
        ]

        return jsonify(response), 200

# -----------------------------
# POST /api/budgets → criar um novo orçamento
# -----------------------------
@budgets_bp.route('/budgets', methods=['POST'])
def create_budget():
    try:
        budget_data = BudgetCreate(**request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    with session_scope() as session:
        month_str = budget_data.month
        year, month = map(int, month_str.split("-"))
        db_date = date(year, month, 1)
        
        new_budget = Budget(
            month=db_date,
            limit=budget_data.limit,
            category_id=budget_data.category_id
        )
        
        session.add(new_budget)
        session.flush()
        session.refresh(new_budget)

        response = BudgetResponse.model_validate(new_budget).model_dump()
        return jsonify(response), 201

# -----------------------------
# PUT /api/budgets/<int: budget_id> → atualizar um orçamento existente
# -----------------------------
@budgets_bp.route("/budgets/<int:budget_id>", methods=["PUT"])
def update_budget(budget_id):
    try:
        budget_data = BudgetCreate(**request.json)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    with session_scope() as session:
        budget = (
            session.query(Budget)
            .filter(Budget.budget_id == budget_id)
            .first()
        )  # Busca o orçamento pelo ID

        if not budget:
            return jsonify({"error": "Budget not found"}), 404
        
        month_str = budget_data.month
        year, month = map(int, month_str.split("-"))
        db_date = date(year, month, 1)

        budget.month = db_date
        budget.limit = budget_data.limit
        budget.category_id = budget_data.category_id

        session.flush()  # Garante que as alterações sejam enviadas ao banco de dados
        response = BudgetResponse.model_validate(budget).model_dump()
        return jsonify(response), 200

# -----------------------------
# DELETE /api/budgets/<int:budget_id> → deletar um orçamento existente com base no ID
# -----------------------------
@budgets_bp.route("/budgets/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id):
    with session_scope() as session:
        budget = (
            session.query(Budget)
            .filter(Budget.budget_id == budget_id)
            .first()
        )

        if not budget:
            return jsonify({"error": "Budget not found"}), 404

        session.delete(budget)

        return jsonify({"message": "Budget deleted successfully"}), 204