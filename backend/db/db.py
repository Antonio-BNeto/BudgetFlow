from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./budgetflow.db"  # ou seu banco real

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)  # Engine do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Sessão do banco de dados

Base = declarative_base()  # Base para os modelos