from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
