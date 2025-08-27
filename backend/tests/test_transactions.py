def test_create_transaction(client):
    cat = client.post('/api/categories', json={'name': 'Groceries'}).get_json()

    response = client.post('/api/transactions', json={
        "type": "expense",
        "amount": 120.75,
        "date": "2024-08-15",
        "description": "Supermarket",
        "category_id": cat['category_id']
    })

    assert response.status_code == 201
    data = response.get_json()
    assert float(data['amount']) == 120.75
    assert data['description'] == "Supermarket"
    assert data['type'] == "expense"

def test_get_transactions(client):
    response = client.get('/api/transactions')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_update_transaction(client):
    cat = client.post('/api/categories', json={'name': 'Transportation'}).get_json()

    transaction_resp = client.post('/api/transactions', json={
        "type": "income",
        "amount": 75.50,
        "date": "2024-08-16",
        "description": "Bus Ticket",
        "category_id": cat['category_id']
    })

    assert transaction_resp.status_code == 201
    transaction = transaction_resp.get_json()

    response = client.put(f'/api/transactions/{transaction["transaction_id"]}', json={
        "type": "income",
        "amount": 5.00,
        "date": "2024-08-16",
        "description": "Metro Ticket",
        "category_id": cat['category_id']
    })

    assert response.status_code == 200
    data = response.get_json()
    assert float(data['amount']) == 5.00
    assert data['description'] == "Metro Ticket"
    assert data['type'] == "income"

def test_delete_transaction(client):
    cat = client.post('/api/categories', json={'name': 'Utilities'}).get_json()

    transaction_resp = client.post('/api/transactions', json={
        "type": "expense",
        "amount": 200.00,
        "date": "2024-08-17",
        "description": "Electricity Bill",
        "category_id": cat['category_id']
    })

    assert transaction_resp.status_code == 201
    transaction = transaction_resp.get_json()

    response = client.delete(f'/api/transactions/{transaction["transaction_id"]}')
    assert response.status_code == 204