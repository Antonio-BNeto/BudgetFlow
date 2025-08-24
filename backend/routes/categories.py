from flask import Blueprint, request, jsonify
from db.db import SessionLocal  # Importa a sessão do banco de dados
from db.models import Category  # Importa o modelo Category

# Criando o blueprint para categorias (conjunto de rotas do recurso Category)
categories_bp = Blueprint('categories', __name__)


# Criar sessão do banco (controla as queries)
def get_db():
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db  # Retorna a sessão para uso
    finally:
        db.close()  # Garante que a sessão seja fechada

# -----------------------------
# GET /api/categories → listar todas as categorias
# -----------------------------
@categories_bp.route('/', methods=['GET'])
def get_categories():
    db = next(get_db())  # Obtém a sessão do banco de dados
    categories = db.query(Category).all()  # Consulta todas as categorias
    return jsonify([{"id": c.id, "name": c.name} for c in categories])  # Retorna as categorias em formato JSON


# -----------------------------
# POST /api/categories → criar uma nova categoria
# -----------------------------
@categories_bp.route('/', methods=['POST'])
def create_category():
    db = next(get_db())
    data = request.json  # Obtém os dados da requisição
    new_category = Category(name=data["name"])  # Cria uma nova categoria

    db.add(new_category)  # Adiciona a nova categoria à sessão
    db.commit() # Salvar as alterações no banco de dados
    db.refresh(new_category)  # Atualiza o objeto com os dados do banco

    return jsonify({"id": new_category.id, "name":new_category.name}), 201  # Retorna a nova categoria criada

# -----------------------------
# PUT /api/categories → Atualizar uma categoria que está no banco
# -----------------------------
@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    db = next(get_db())
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    data = request.json  # Obtém os dados da requisição
    category.name = data.get("name", category.name) # Atualiza o nome da categoria
    db.commit() # Salvar as alterações no banco de dados

    return jsonify({"id": category.id, "name": category.name}) # Retorna a categoria atualizada

# -----------------------------
# DELETE /api/categories → Deleta uma categoria que está no banco
# -----------------------------
@categories_bp.route("<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    db = next(get_db())
    category = db.query(Category).filter(Category.id == category_id).first() 
    
    if not category:
        return jsonify({"error": "Category not found"}), 404
     
    db.delete(category) # Deleta categoria
    db.commit() # Salvar as alterações

    return jsonify({"Message": "Category deleted successfully"})