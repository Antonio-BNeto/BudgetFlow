from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# -----------------------------------------------------------------------------
# 1) URL do banco (direto no código)
#    Você pode trocar para PostgreSQL, MySQL etc. se precisar.
# -----------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./budgetflow.db"  # ou seu banco real

# Para SQLite, é necessário um argumento especial chamado "check_same_thread"
# que permite que a conexão seja compartilhada entre diferentes threads.
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# -----------------------------------------------------------------------------
# 2) Engine (conexão de baixo nível com o banco)
# -----------------------------------------------------------------------------
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)

# -----------------------------------------------------------------------------
# 3) SessionLocal (fábrica de sessões) e Base (classe base para os modelos)
# -----------------------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------------------------------------------------------
# 4)get_db(): gerador de sessão
# -----------------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------------------------------------------------------
# 5) session_scope(): context manager com commit/rollback automático
# -----------------------------------------------------------------------------
@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# -----------------------------------------------------------------------------
# 6) init_db(): cria as tabelas no banco de dados com base nos modelos
# -----------------------------------------------------------------------------
def init_db():
    from db import models  # Importa os modelos para registrar as tabelas
    Base.metadata.create_all(bind=engine)
