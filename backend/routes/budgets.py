from flask import Blueprint, request, jsonify
from db.db import SessionLocal  # Importa a sessão do banco de dados
from db.models import Budget  # Importa o modelo Budgets

# Criando o blueprint para orçamentos (conjunto de rotas do recurso Budget)
budgets_bp = Blueprint('budgets', __name__)

def get_db():
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db  # Retorna a sessão para uso
    finally:
        db.close()  # Garante que a sessão seja fechada

# -----------------------------
# GET /api/budgets → listar todos os orçamentos
# -----------------------------
@budgets_bp.route('/', methods=['GET'])
def get_budgets():
    db = next(get_db())
    budgets = db.query(Budget).all() # Retorna uma lista com todos os orçamentos

    return jsonify([{"id": b.id_budget, "month": b.month, "limit": b.limit, "category": b.category.name} for b in budgets])

# -----------------------------
# POST /api/budgets → criar um novo orçamento
# -----------------------------
@budgets_bp.route('/', methods=['POST'])
def create_budget():
    db = next(get_db())
    
    data = request.json  # Obtém os dados da requisição

    new_budget = Budget(**data) # Cria uma nova instancia do orçamento (**data) faz uma atribuição dos valores do dicionário data para os atributos do objeto Budget
    
    db.add(new_budget)  # Adiciona o novo orçamento à sessão
    db.commit() # Salva a nova instância do orçamento no banco de dados
    
    db.refresh(new_budget)  # Atualiza o objeto com os dados do banco
    
    return jsonify({"id": new_budget.id_budget, "month": new_budget.month, "limit": new_budget.limit, "category": new_budget.category.name}), 201  # Retorna o novo orçamento criado

# -----------------------------
# PUT /api/budgets → atualizar um orçamento existente
# -----------------------------
@budgets_bp.route("<int:id_budget>", methods=["PUT"])
def update_budget(id_budget):
    db = next(get_db())

    budget = db.query(Budget).filter(Budget.id_budget == id_budget).first()  # Busca o orçamento pelo ID

    if not budget:
        return jsonify({"error": "Budget not found"}) , 404
    
    data = request.json  # Obtém os dados da requisição

    # Atualiza os atributos do orçamento com os novos dados
    for key, value in data.items():
        setattr(budget, key, value)


    db.commit()  # Salva as alterações no banco de dados
    db.refresh(budget)  # Atualiza o objeto com os dados do banco

    return jsonify({"id": budget.id_budget, "month": budget.month, "limit": budget.limit, "category": budget.category.name})

# -----------------------------
# DELETE /api/budgets → deletar um orçamento existente
# -----------------------------