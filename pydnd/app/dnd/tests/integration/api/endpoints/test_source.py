"""Integration Testing Endpoint: /sources."""

import random

import pytest
from dnd import models, schemas
from dnd.core import uncached_settings
from dnd.tests.integration import helpers
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_source(integration_global_data) -> schemas.source.SourceCreate:
    """Returns a random source from global test data and keeps that reference for the module."""
    r_source = random.choice(integration_global_data.get("source"))
    random_source = schemas.source.SourceCreate(**r_source)
    return random_source


def test_post(client: TestClient, random_source: schemas.source.SourceCreate) -> None:
    """Tests post: happy path."""
    response = client.post(f"{uncached_settings.API_V1_STR}/sources", json=random_source.model_dump())
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json == random_source.model_dump()


def test_get(client: TestClient) -> None:
    """Tests get: happy path."""
    response = client.get(f"{uncached_settings.API_V1_STR}/sources")
    response_schema = schemas.responses.GenericListResponse[schemas.source.SourceBase](**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert len(response_schema.data) > 0


def test_put(client: TestClient, random_source: schemas.source.SourceCreate) -> None:
    """Tests put: happy path."""
    random_source_copy = schemas.source.SourceCreate(**random_source.model_dump())
    random_source_copy.short_name = "testing_update"
    response = client.put(f"{uncached_settings.API_V1_STR}/sources", json=random_source_copy.model_dump())
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json.get("short_name") == random_source_copy.short_name


def test_put_does_not_exist(client: TestClient, random_source: schemas.source.SourceCreate) -> None:
    """Tests post: 404."""
    random_source_copy = schemas.source.SourceCreate(**random_source.model_dump())
    random_source_copy.id = -999999999
    response = client.put(f"{uncached_settings.API_V1_STR}/sources", json=random_source_copy.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete(client: TestClient, random_source: schemas.source.SourceCreate) -> None:
    """Tests delete: happy path."""
    response = client.delete(f"{uncached_settings.API_V1_STR}/sources?id={random_source.id}")
    message = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "message" in message


def test_delete_does_not_exist(client: TestClient, random_source: schemas.source.SourceCreate) -> None:
    """Tests delete: 404."""
    random_source_copy = schemas.source.SourceCreate(**random_source.model_dump())
    random_source_copy.id = -999999999
    response = client.delete(f"{uncached_settings.API_V1_STR}/sources?id={random_source_copy.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("count", range(2))
def test_post_bulk(client: TestClient, test_data_directory: str, count) -> None:
    """Test /bulk post: happy path -> runs twice to test idempotence."""
    assert count is not None, "avoiding W0613: unused-argument"
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
    bulk_load_response = schemas.responses.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored == 0


def test_post_bulk_bad_filetype(client: TestClient, test_data_directory: str) -> None:
    """Test /bulk post: illegal file type (foo/bar)."""
    files = {
        "upload_file": (
            "source.json",
            open(f"{test_data_directory}/json/seeds/source.json", "rb"),
            "foo/bar",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/sources/bulk",
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
        f"{uncached_settings.API_V1_STR}/sources/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    bulk_load_response = schemas.responses.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored > 0


def test_clean_up(client: TestClient, db: Session) -> None:
    """Remove anything added from this test file."""
    helpers.purge_table(client, db, models.Source, "sources")
