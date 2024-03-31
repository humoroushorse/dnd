"""Integration testing setup and pytest fixtures."""

import json
import random
import sys
from os import path
from typing import Generator

import pytest
from dnd.api.deps import get_db
from dnd.core import uncached_settings
from dnd.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(uncached_settings.SQLALCHEMY_TESTING_DATABASE_URI, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override default database with testing database."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def pytest_addoption(parser):
    """Custom pytest flags."""
    parser.addoption("--seed", action="store", default="")
    parser.addoption("--skip-d20", action="store", default=False)


@pytest.fixture()
def skip_d20(request) -> bool:
    """Pytest Fixture: returns if tests should skip the d20 roll test."""
    skip_d20: bool = request.config.getoption("--skip-d20")
    return bool(skip_d20)


@pytest.fixture(scope="session", autouse=True)
def random_seed(request) -> any:
    """Pytest Fixture (autouse): Random is seeded and can be ran with that seed for debugging tests on failure."""
    seed_str = request.config.getoption("--seed")
    if seed_str.isnumeric():
        seed = int(seed_str)
    else:
        seed = random.randrange(sys.maxsize)
    random.seed(seed)
    print(f"Running tests with seed: {seed}")  # noqa: T201


@pytest.fixture(scope="session")
def test_data_directory() -> str:
    """Pytest Fixture: get the base directory str path for ~/pydnd/app/dnd/test_data."""
    basepath = path.dirname(__file__)
    test_data_root = path.abspath(path.join(basepath, "..", "..", "test_data"))
    yield test_data_root


@pytest.fixture(scope="module")
def integration_global_data(test_data_directory: str):
    """A global dictionary of test data to be shared by integration tests."""

    def load_json_from_file(file: str) -> any:
        """Gets a json object from a file."""
        with open(f"{test_data_directory}/json/seeds/{file}") as file_input:  # pylint: disable=unspecified-encoding
            as_json = json.load(file_input)
            return as_json

    sources = load_json_from_file("source.json")
    classes = load_json_from_file("class.json")
    spells_phb = load_json_from_file("spells_phb.json")
    spells_xanathars = load_json_from_file("spells_xanathars.json")
    spells_tashas = load_json_from_file("spells_tashas.json")
    spell_to_class_phb = load_json_from_file("spell_to_class_phb.json")
    spell_to_class_xanathars = load_json_from_file("spell_to_class_xanathars.json")
    spell_to_class_tashas = load_json_from_file("spell_to_class_tashas.json")
    yield {
        "source": [*sources],
        "dnd_class": [*classes],
        "spell": [*spells_phb, *spells_xanathars, *spells_tashas],
        "spell_to_class": [
            *spell_to_class_phb,
            *spell_to_class_xanathars,
            *spell_to_class_tashas,
        ],
    }


@pytest.fixture(scope="session")
def db() -> Generator:
    """Pytest Fixture: reference to the testing sqlalchemy.orm.Session."""
    yield TestingSessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    """Pytest Fixture: reference to the TestClient."""
    with TestClient(app) as c:
        yield c
