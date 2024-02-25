"""Integration Testing Endpoint: /spell-to-class."""

import random

import pytest
from app.dnd import models, schemas
from app.dnd.core import uncached_settings
from app.dnd.tests.integration import helpers
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_source(integration_global_data: dict) -> schemas.source.SourceCreate:
    """Returns a random source from global test data and keeps that reference for the module."""
    r_source = random.choice(integration_global_data.get("source"))
    random_source = schemas.source.SourceCreate(**r_source)
    return random_source


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_dnd_class(
    integration_global_data: dict,
    random_source: schemas.source.SourceCreate,
) -> schemas.dnd_class.DndClassCreate:
    """Returns a random dnd_class from global test data and keeps that reference for the module."""
    r_class = random.choice(integration_global_data.get("dnd_class"))
    random_dnd_class = schemas.dnd_class.DndClassCreate(**r_class)
    random_dnd_class.source_id = random_source.id
    return random_dnd_class


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_spell(
    integration_global_data: dict,
    random_source: schemas.source.SourceCreate,
) -> schemas.spell.SpellCreate:
    """Returns a random spell from global test data and keeps that reference for the module."""
    r_source = random.choice(integration_global_data.get("spell"))
    random_spell = schemas.spell.SpellCreate(**r_source)
    random_spell.id = 0
    random_spell.source_id = random_source.id
    return random_spell


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_spell_to_class(
    random_source: schemas.source.SourceCreate,
    random_spell: schemas.spell.SpellBase,
    random_dnd_class: schemas.dnd_class.DndClassCreate,
) -> schemas.jt_spell_to_class.JtSpellToClassCreate:
    """Returns a random dnd_class from global test data and keeps that reference for the module."""
    jt_spell_to_class = schemas.jt_spell_to_class.JtSpellToClassCreate(
        id=0,
        source_id=random_source.id,
        source_name=random_source.name,
        dnd_class_id=random_dnd_class.id,
        dnd_class_name=random_dnd_class.name,
        spell_id=random_spell.id,
        spell_name=random_spell.name,
    )
    return jt_spell_to_class


def test_set_up(
    client: TestClient,
    test_data_directory: str,
    random_spell: schemas.spell.SpellBase,
) -> None:
    """Set up required foreign key data: [source]."""
    # load in all sources
    helpers.bulk_load_file(client, f"{test_data_directory}/json/seeds/source.json", "sources")
    # load in random spell
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spells",
        json=jsonable_encoder(random_spell.dict()),
    )
    assert response.status_code == status.HTTP_200_OK
    # load in all xanathars spells
    helpers.bulk_load_file(client, f"{test_data_directory}/json/seeds/spells_xanathars.json", "spells")
    # load in all classes
    helpers.bulk_load_file(client, f"{test_data_directory}/json/seeds/class.json", "classes")


def test_post(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test post: happy path."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassCreate(
        id=random_spell_to_class.id,
        source_name=random_spell_to_class.source_name,
        dnd_class_name=random_spell_to_class.dnd_class_name,
        spell_name=random_spell_to_class.spell_name,
    )
    expected = schemas.jt_spell_to_class.JtSpellToClassBase(
        id=random_spell_to_class.id,
        source_id=random_spell_to_class.source_id,
        dnd_class_id=random_spell_to_class.dnd_class_id,
        spell_id=random_spell_to_class.spell_id,
    )
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json == expected.dict()


def test_post_invalid_source_name(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test post: happy path."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassCreate(
        id=random_spell_to_class.id,
        source_name="SOME INVALID SOURCE NAME",
        dnd_class_name=random_spell_to_class.dnd_class_name,
        spell_name=random_spell_to_class.spell_name,
    )
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_invalid_dnd_class_name(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test post: happy path."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassCreate(
        id=random_spell_to_class.id,
        source_name=random_spell_to_class.source_name,
        dnd_class_name="SOME INVALID DND CLASS NAME",
        spell_name=random_spell_to_class.spell_name,
    )
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_invalid_spell_name(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test post: happy path."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassCreate(
        id=random_spell_to_class.id,
        source_name=random_spell_to_class.source_name,
        dnd_class_name=random_spell_to_class.dnd_class_name,
        spell_name="SOME INVALID SPELL NAME",
    )
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get(client: TestClient) -> None:
    """Test get: happy path."""
    response = client.get(f"{uncached_settings.API_V1_STR}/spell-to-class")
    response_schema = schemas.responses.GenericListResponse[schemas.jt_spell_to_class.JtSpellToClassBase](
        **response.json()
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response_schema.data) > 0


def test_put(
    client: TestClient,
    random_source: schemas.source.SourceBase,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
    integration_global_data: dict,
) -> None:
    """Test put: happy path."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassBase(**random_spell_to_class.dict())
    # since we loaded in all sources, get all source ids and chose one that doesnt match our random_source id
    filtered_ids = [
        source.get("id") for source in integration_global_data.get("source") if source.get("id") != random_source.id
    ]
    random_id = random.choice(filtered_ids)
    random_spell_to_class_copy.source_id = random_id
    response = client.put(
        url=f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    response_schema = schemas.jt_spell_to_class.JtSpellToClassBase(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response_schema.source_id == random_id


def test_put_does_not_exist(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test put: 404."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassBase(**random_spell_to_class.dict())
    random_spell_to_class_copy.id = -999999999
    response = client.put(
        url=f"{uncached_settings.API_V1_STR}/spell-to-class",
        json=random_spell_to_class_copy.dict(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test delete: happy path."""
    response = client.delete(f"{uncached_settings.API_V1_STR}/spell-to-class?id={random_spell_to_class.id}")
    message = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "message" in message


def test_delete_does_not_exist(
    client: TestClient,
    random_spell_to_class: schemas.jt_spell_to_class.JtSpellToClassCreate,
) -> None:
    """Test delete: 404."""
    random_spell_to_class_copy = schemas.jt_spell_to_class.JtSpellToClassBase(**random_spell_to_class.dict())
    random_spell_to_class_copy.id = -999999999
    response = client.delete(f"{uncached_settings.API_V1_STR}/spell-to-class?id={random_spell_to_class_copy.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("count", range(2))
def test_post_bulk(client: TestClient, test_data_directory: str, count) -> None:
    """Test /bulk post: happy path -> runs twice to test idempotence."""
    assert count is not None, "avoiding W0613: unused-argument"
    files = {
        "upload_file": (
            "spell_to_class_xanathars.json",
            open(f"{test_data_directory}/json/seeds/spell_to_class_xanathars.json", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    bulk_load_response = schemas.responses.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored == 0


def test_post_bulk_bad_filetype(client: TestClient, test_data_directory: str) -> None:
    """Test /bulk post: illegal file type (foo/bar)."""
    files = {
        "upload_file": (
            "spell_to_class_xanathars.json",
            open(f"{test_data_directory}/json/seeds/spell_to_class_xanathars.json", "rb"),
            "foo/bar",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spell-to-class/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    response_json: dict = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "foo/bar" in response_json.get("detail")


# def test_post_bulk_bad_json_data(client: TestClient, test_data_directory: str) -> None:
#     """Test /bulk post: illegal data set -> list with empty dict."""
#     files = {
#         "upload_file": (
#             "empty_json_in_array.json",
#             open(f"{test_data_directory}/json/invalid/empty_json_in_array.json", "rb"),
#             "application/json",
#         )
#     }
#     response = client.post(
#         f"{settings.API_V1_STR}/spell-to-class/bulk",
#         files=files,
#         headers={"accept": "application/json"},
#     )
#     bulk_load_response = schemas.responses.BulkLoadResponse(**response.json())
#     assert response.status_code == status.HTTP_200_OK
#     assert bulk_load_response.totals.errored > 0


def test_clean_up(client: TestClient, db: Session) -> None:
    """Remove anything added from this test file."""
    helpers.purge_table(client, db, models.JtSpellToClass, "spell-to-class")
    helpers.purge_table(client, db, models.Spell, "spells")
    helpers.purge_table(client, db, models.DndClass, "classes")
    helpers.purge_table(client, db, models.Source, "sources")
