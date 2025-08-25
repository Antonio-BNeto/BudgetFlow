import datetime
from db.db import init_db, session_scope
from db import models

def test_db_operations():
    # Inicializa banco e tabelas
    init_db()
    
    # 1) Insere categoria
    with session_scope() as db:
        cat = models.Category(name="Alimentação")
        db.add(cat)

    # 2) Insere orçamento
    with session_scope() as db:
        category = db.query(models.Category).filter_by(name="Alimentação").first()
        budget = models.Budget(month="2024-06", limit=1500.0, category_id=category.category_id)
        db.add(budget)
    
    # 3) Insere transação
    with session_scope() as db:
        category = db.query(models.Category).filter_by(name="Alimentação").first()
        transaction = models.Transaction(
            type=models.TransactionType.expense,
            amount=50.0,
            date=datetime.date.today(),
            description="Supermercado",
            category_id=category.category_id
        )
        db.add(transaction)
        
    # 4) Consulta e valida
    with session_scope() as db:
        categories = db.query(models.Category).all()
        budgets = db.query(models.Budget).all()
        transactions = db.query(models.Transaction).all()

        assert len(categories) == 1
        assert categories[0].name == "Alimentação"

        assert len(budgets) == 1
        assert budgets[0].month == "2024-06"
        assert budgets[0].limit == 1500.0

        assert len(transactions) == 1
        assert transactions[0].amount == 50.0
        assert transactions[0].description == "Supermercado"