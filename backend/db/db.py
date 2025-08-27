from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager

# -----------------------------------------------------------------------------
# 1) Instância global do SQLAlchemy
# -----------------------------------------------------------------------------
db = SQLAlchemy()

# -----------------------------------------------------------------------------
# 2) Context manager de sessão
#    Permite usar `with session_scope() as db:` para commit/rollback automático
# ----------------------------------------------------------------------------- 
@contextmanager
def session_scope():
    session = db.session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# -----------------------------------------------------------------------------
# 3) Função auxiliar para obter uma sessão manualmente
# -----------------------------------------------------------------------------
def get_db():
    
    session = db.session()
    try:
        yield session
    finally:
        session.close()