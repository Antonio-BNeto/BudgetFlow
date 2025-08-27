import pytest
import os
import tempfile
from app import app as flask_app, db

@pytest.fixture(scope='session')
def app():

    db_fd, db_path = tempfile.mkstemp()

    # Banco só em memória (não vai criar arquivo físico)
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()