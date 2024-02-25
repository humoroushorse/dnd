"""Unit testing setup and pytest fixtures."""

from typing import Generator

import pytest
from app.dnd.api.deps import get_db
from app.dnd.database.base import DbBase
from app.dnd.database.session import SessionLocal
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ...main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# @event.listens_for(engine, "first_connect")
# def schema_attach(dbapi_connection, connection_record) -> None:
# def schema_attach(dbapi_connection) -> None:
#     dbapi_connection.execute("ATTACH DATABASE 'dnd.db' AS dnd")


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DbBase.metadata.create_all(bind=engine)


def override_get_db() -> Session:
    """Override default database with testing database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db() -> Generator:
    """Pytest Fixture: reference to the testing sqlalchemy.orm.Session."""
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    """Pytest Fixture: reference to the TestClient."""
    with TestClient(app) as c:
        yield c
