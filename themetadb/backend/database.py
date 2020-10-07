# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.realpath(os.path.join(os.getcwd(), 'test.db'))
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# db = SQLAlchemy(app)


def get_db():
    # FastAPI Dependency
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
