import pytest 
from app import app
from db.db import Base, engine

# configura o cliente de teste do Flask
@pytest.fixture
def client():
    # Ativa o modo de teste
    app.config['TESTING'] = True

    # Cria as tabelas (em memória ou no DB configurado em db/db.py)
    Base.metadata.create_all(bind=engine)

    with app.test_client() as client:
        yield client

    # Limpa  as tabelas depois dos testes
    Base.metadata.drop_all(bind=engine)

# -----------------------------
# Teste: criar categoria
# -----------------------------
def test_create_category(client):
    response = client.post('/api/categories', json={'name': 'Transporte'})
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['name'] == 'Transporte'
    assert 'category_id' in data #garante que o ID foi gerado

# -----------------------------
# Teste: listar categorias
# -----------------------------
def test_get_categories(client):
    # Primeiro cria uma categoria para garantir que haja pelo menos uma categoria
    client.post('/api/categories', json={'name': 'Alimentação'})
    
    response = client.get('/api/categories')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert any(c['name'] == 'Alimentação' for c in data) # verifica se a categoria está na lista