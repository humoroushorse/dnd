"""Integration Testing Endpoint: /spells."""
import random

import pytest
from dnd import models, schemas
from dnd.core import uncached_settings
from dnd.tests.integration import helpers
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# spells_phb.json adds like 3-4 seconds to the integration tests runtime
BULK_SPELLS_SEEDS_FILE = "spells_tashas.json"


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_spell(integration_global_data) -> schemas.spell.SpellCreate:
    """Returns a random spell from global test data and keeps that reference for the module."""
    r_source = random.choice(integration_global_data.get("spell"))
    random_spell = schemas.spell.SpellCreate(**r_source)
    random_spell.id = 0
    return random_spell


def assert_dict_equals_spell(spell_a: dict, spell_b: dict) -> None:
    """Removes dict fields that are changed by the system for testing equality."""
    a = {**spell_a}
    del a["created_at"]
    del a["updated_at"]
    b = {**spell_b}
    del b["created_at"]
    del b["updated_at"]
    assert a == b


def test_set_up(client: TestClient, test_data_directory: str) -> None:
    """Set up required foreign key data: [source]."""
    # load in sources
    files = {
        "upload_file": (
            "source.json",
            open(f"{test_data_directory}/json/seeds/source.json", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/sources/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    response_json: dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json.get("totals", {}).get("errored") == 0


def test_post(client: TestClient, random_spell: schemas.spell.SpellCreate) -> None:
    """Test post: happy path."""
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spells",
        json=jsonable_encoder(random_spell.dict()),
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert_dict_equals_spell(response_json, random_spell.dict())


def test_get(client: TestClient) -> None:
    """Test get: happy path."""
    response = client.get(f"{uncached_settings.API_V1_STR}/spells")
    response_schema = schemas.responses.GenericListResponse[schemas.spell.SpellBase](
        **response.json()
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response_schema.data) > 0


def test_put(client: TestClient, random_spell: schemas.spell.SpellCreate) -> None:
    """Test put: happy path."""
    random_spell_copy = schemas.spell.SpellCreate(**random_spell.dict())
    random_spell_copy.description = "testing_update"
    response = client.put(
        f"{uncached_settings.API_V1_STR}/spells",
        json=jsonable_encoder(random_spell_copy.dict()),
    )
    response_json: dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json.get("description") == random_spell_copy.description


def test_put_does_not_exist(
    client: TestClient, random_spell: schemas.spell.SpellCreate
) -> None:
    """Test put: 404."""
    random_spell_copy = schemas.spell.SpellCreate(**random_spell.dict())
    random_spell_copy.id = -999999999
    response = client.put(
        f"{uncached_settings.API_V1_STR}/spells",
        json=jsonable_encoder(random_spell_copy.dict()),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete(client: TestClient, random_spell: schemas.spell.SpellCreate) -> None:
    """Test delete: happy path."""
    response = client.delete(
        f"{uncached_settings.API_V1_STR}/spells?id={random_spell.id}"
    )
    message = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "message" in message


def test_delete_does_not_exist(
    client: TestClient, random_spell: schemas.spell.SpellCreate
) -> None:
    """Test delete: 404."""
    random_spell_copy = schemas.spell.SpellCreate(**random_spell.dict())
    random_spell_copy.id = -999999999
    response = client.delete(
        f"{uncached_settings.API_V1_STR}/spells?id={random_spell_copy.id}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("count", range(2))
def test_post_bulk(client: TestClient, test_data_directory: str, count) -> None:
    """Test /bulk post: happy path -> runs twice to test idempotence."""
    assert count is not None, "avoiding W0613: unused-argument"
    files = {
        "upload_file": (
            BULK_SPELLS_SEEDS_FILE,
            open(f"{test_data_directory}/json/seeds/{BULK_SPELLS_SEEDS_FILE}", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spells/bulk",
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
            BULK_SPELLS_SEEDS_FILE,
            open(f"{test_data_directory}/json/seeds/{BULK_SPELLS_SEEDS_FILE}", "rb"),
            "foo/bar",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spells/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    response_json: dict = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "foo/bar" in response_json.get("detail")


def test_post_bulk_bad_json_data(client: TestClient, test_data_directory: str) -> None:
    """Test /bulk post: illegal data set -> list with empty dict."""
    files = {
        "upload_file": (
            "empty_json_in_array.json",
            open(f"{test_data_directory}/json/invalid/empty_json_in_array.json", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/spells/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    bulk_load_response = schemas.responses.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored > 0


def test_clean_up(client: TestClient, db: Session) -> None:
    """Remove anything added from this test file."""
    helpers.purge_table(client, db, models.Spell, "spells")
    helpers.purge_table(client, db, models.Source, "sources")
