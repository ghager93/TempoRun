import os

from sqlmodel import create_engine, SQLModel, Session

from app.conf import config


DATABASE_URI = f"sqlite:///{config.get('db_path')}"

engine = create_engine(DATABASE_URI, echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})


def _yield_session():
    with Session(engine) as session:
        yield session


def get_session():
    return next(_yield_session())