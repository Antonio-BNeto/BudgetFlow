from flask import Blueprint, request, jsonify
from db.db import session_scope  # Importa a sessão do banco de dados
from db.models import Category  # Importa o modelo Category

# Criando o blueprint para categorias (conjunto de rotas do recurso Category)
categories_bp = Blueprint('categories', __name__)

# -----------------------------
# GET /api/categories → listar todas as categorias
# -----------------------------
@categories_bp.route('/', methods=['GET'])
def get_categories():
    with session_scope() as db:
        categories = db.query(Category).all()  # Consulta todas as categorias
        return jsonify([{"category_id": c.category_id, "name": c.name} for c in categories])  # Retorna as categorias em formato JSON


# -----------------------------
# POST /api/categories → criar uma nova categoria
# -----------------------------
@categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.json  # Obtém os dados da requisição
    with session_scope() as db:
        existing = db.query(Category).filter(Category.name == data["name"]).first()  # Consulta se a categoria já existe
    
        if existing:
            return jsonify({"error": "Category already exists"}), 400

        new_category = Category(name=data["name"])  # Cria uma nova categoria
        db.add(new_category)  # Adiciona a nova categoria à sessão
        db.flush()  # Garante que a nova categoria tenha um ID gerado

        return jsonify({"category_id": new_category.category_id, "name":new_category.name}), 201  # Retorna a nova categoria criada

# -----------------------------
# PUT /api/categories/<int:category_id> → Atualizar uma categoria que está no banco
# -----------------------------
@categories_bp.route("/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    data = request.json  # Obtém os dados da requisição
    with session_scope() as db:
        category = db.query(Category).filter(Category.id == category_id).first()

        if not category:
            return jsonify({"error": "Category not found"}), 404

        category.name = data.get("name", category.name)  # Atualiza o nome da categoria
        db.flush()

        return jsonify({"category_id": category.category_id, "name": category.name})  # Retorna a categoria atualizada

# -----------------------------
# DELETE /api/categories/<int:category_id> → Deleta uma categoria que está no banco
# -----------------------------
@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    with session_scope() as db:
        category = db.query(Category).filter(Category.category_id == category_id).first()

        if not category:
            return jsonify({"error": "Category not found"}), 404

        db.delete(category)  # Deleta categoria

        return jsonify({"Message": "Category deleted successfully"})