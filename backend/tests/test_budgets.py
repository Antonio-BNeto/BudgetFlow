import pytest
from app import app
from db.db import Base, engine

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    Base.metadata.create_all(bind=engine)
    
    with app.test_client() as client:
        yield client

    Base.metadata.drop_all(bind=engine)
    
# -----------------------------
# Teste: criar orçamento
# -----------------------------
def test_create_budget(client):
    cat_resp = client.post('/api/categories', json={'name': 'Trasporte'})
    category_id = cat_resp.get_json()['category_id']
    
    response = client.post('/api/budgets', json={
        'month': '2025-08',
        'limit': 1500.0,
        'category_id': category_id
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['month'] == '2025-08'
    assert data['limit'] == 1500.0
    assert data['category_id'] == category_id
    assert 'budget_id' in data