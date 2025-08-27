# -----------------------------
# Teste: criar categoria
# -----------------------------
def test_create_category(client):
    response = client.post('/api/categories', json={'name': 'Food'})
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['name'] == 'Food'

# -----------------------------
# Teste: listar categorias
# -----------------------------
def test_get_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(cat['name'] == 'Food' for cat in data)

# -----------------------------
# Teste: Atualizar categoria
# -----------------------------
def test_update_category(client):
    # Primeiro cria uma categoria para garantir que haja pelo menos uma categoria
    create_resp = client.post('/api/categories', json={'name': 'Transport'})
    category_id = create_resp.get_json()['category_id']

    # Atualiza a categoria
    update_resp = client.put(f'/api/categories/{category_id}', json={'name': 'Entertainment'})
    assert update_resp.status_code == 200
    assert update_resp.get_json()['name'] == 'Entertainment'

# -----------------------------
# Teste: Deletar categoria
# -----------------------------
def test_delete_category(client):
    # Primeiro cria uma categoria para garantir que haja pelo menos uma categoria
    create_resp = client.post('/api/categories', json={'name': 'ToDelete'})
    category_id = create_resp.get_json()['category_id']
    
    delete_resp = client.delete(f'/api/categories/{category_id}')
    assert delete_resp.status_code == 204