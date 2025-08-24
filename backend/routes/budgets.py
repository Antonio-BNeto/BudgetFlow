from flask import Blueprint, request, jsonify
from db.db import session_scope  # Importa o gerenciador de contexto da sessão
from db.models import Budget  # Importa o modelo Budgets

# Criando o blueprint para orçamentos (conjunto de rotas do recurso Budget)
budgets_bp = Blueprint('budgets', __name__)

# -----------------------------
# GET /api/budgets → listar todos os orçamentos
# -----------------------------
@budgets_bp.route('/', methods=['GET'])
def get_budgets():
    with session_scope() as db:
        budgets = db.query(Budget).all() # Retorna uma lista com todos os orçamentos

    return jsonify([
        {
            "budget_id": b.budget_id,
            "month": b.month,
            "limit": b.limit,
            "category": b.category.name
        } 
        for b in budgets
    ])

# -----------------------------
# POST /api/budgets → criar um novo orçamento
# -----------------------------
@budgets_bp.route('/', methods=['POST'])
def create_budget():
    
    data = request.json  # Obtém os dados da requisição
    
    with session_scope() as db:
        new_budget = Budget(**data) # Cria uma nova instancia do orçamento (**data) faz uma atribuição dos valores do dicionário data para os atributos do objeto Budget
        db.add(new_budget)  # Adiciona o novo orçamento à sessão
        db.flush() # Garante que o novo orçamento tenha um ID gerado
        
        db.refresh(new_budget)  # Atualiza o objeto com os dados do banco
    
    return jsonify({
        "budget_id": new_budget.budget_id,
        "month": new_budget.month,
        "limit": new_budget.limit,
        "category": new_budget.category.name
    }), 201  # Retorna o novo orçamento criado

# -----------------------------
# PUT /api/budgets/<int: budget_id> → atualizar um orçamento existente
# -----------------------------
@budgets_bp.route("/<int:budget_id>", methods=["PUT"])
def update_budget(budget_id):
    data = request.json  # Obtém os dados da requisição

    with session_scope() as db:
        budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()  # Busca o orçamento pelo ID

        if not budget:
            return jsonify({"error": "Budget not found"}), 404
        
        # Atualiza os atributos do orçamento com os novos dados
        for key, value in data.items():
            setattr(budget, key, value)

        db.flush()  # Garante que as alterações sejam enviadas ao banco de dados
        db.refresh(budget)  # Atualiza o objeto com os dados do banco

    return jsonify({
        "budget_id": budget.budget_id,
        "month": budget.month,
        "limit": budget.limit,
        "category": budget.category.name if budget.category else None
    })

# -----------------------------
# DELETE /api/budgets/<int:budget_id> → deletar um orçamento existente com base no ID
# -----------------------------
@budgets_bp.route("/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id):
    with session_scope() as db:
        budget = db.query(Budget).filter(Budget.budget_id == budget_id).first()

        if not budget:
            return jsonify({"error": "Budget not found"}), 404

        db.delete(budget)
        db.flush()

        return jsonify({"message": f"Budget {budget_id} deleted successfully"}), 204