# -----------------------------
# Teste: criar orçamento
# -----------------------------
def test_create_budget(client):
    cat = client.post('/api/categories', json={'name': 'Moradia'}).get_json()
    
    response = client.post('/api/budgets', json={
        "month": "2025-08",
        "limit": 1500.00,
        "category_id": cat['category_id']
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['month'] == "2025-08"
    assert data['limit'] == 1500.00

# -----------------------------
# Teste: listar orçamentos
# -----------------------------
def test_get_budgets(client):
    response = client.get('/api/budgets')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
# -----------------------------
# Teste: Atualizar orçamento
# -----------------------------
def test_update_budget(client):
    cat = client.post('/api/categories', json={'name': 'Educação'}).get_json()

    budget = client.post('/api/budgets', json={
        "month": "2024-02",
        "limit": 800.00,
        "category_id": cat['category_id']
    }).get_json()

    update_resp = client.put(f'/api/budgets/{budget["budget_id"]}', json={
        "month": "2024-03",
        "limit": 900.00,
        "category_id": cat['category_id']
    })
    assert update_resp.status_code == 200
    data = update_resp.get_json()
    assert data['month'] == "2024-03"
    assert data['limit'] == 900.00

# -----------------------------
# Teste: Deletar orçamento
# -----------------------------
def test_delete_budget(client):
    cat = client.post('/api/categories', json={'name': 'Viagem'}).get_json()

    budget = client.post('/api/budgets', json={
        "month": "2024-02",
        "limit": 300.00,
        "category_id": cat['category_id']
    }).get_json()
    
    response = client.delete(f'/api/budgets/{budget["budget_id"]}')
    assert response.status_code == 204