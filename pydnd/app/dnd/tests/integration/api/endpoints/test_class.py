"""Integration Testing Endpoint: /classes."""
import random

import pytest
from dnd import models, schemas
from dnd.core import settings
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# TODO: re-evaluate scope?
@pytest.fixture(scope="module")
def random_dnd_class(integration_global_data) -> schemas.DndClassCreate:
    """Returns a random dnd_class from global test data and keeps that reference for the module."""
    r_source = random.choice(integration_global_data.get("dnd_class"))
    random_dnd_class = schemas.DndClassCreate(**r_source)
    return random_dnd_class


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
        f"{settings.API_V1_STR}/sources/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    response_json: dict = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json.get("totals", {}).get("errored") == 0


def test_post(client: TestClient, random_dnd_class: schemas.DndClassCreate) -> None:
    """Test post: happy path."""
    response = client.post(
        f"{settings.API_V1_STR}/classes", json=random_dnd_class.dict()
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json == random_dnd_class.dict()


def test_get(client: TestClient) -> None:
    """Test get: happy path."""
    response = client.get(f"{settings.API_V1_STR}/classes")
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_json.get("data")) > 0


def test_put(client: TestClient, random_dnd_class: schemas.DndClassCreate) -> None:
    """Test put: happy path."""
    random_dnd_class_copy = schemas.DndClassCreate(**random_dnd_class.dict())
    random_dnd_class_copy.description = "testing_update"
    response = client.put(
        f"{settings.API_V1_STR}/classes", json=random_dnd_class_copy.dict()
    )
    product = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert product.get("description") == random_dnd_class_copy.description


def test_put_does_not_exist(
    client: TestClient, random_dnd_class: schemas.DndClassCreate
) -> None:
    """Test post: 404."""
    random_dnd_class_copy = schemas.DndClassCreate(**random_dnd_class.dict())
    random_dnd_class_copy.id = -999999999
    response = client.put(
        f"{settings.API_V1_STR}/classes", json=random_dnd_class_copy.dict()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete(client: TestClient, random_dnd_class: schemas.DndClassCreate) -> None:
    """Test delete: happy path."""
    response = client.delete(f"{settings.API_V1_STR}/classes?id={random_dnd_class.id}")
    message = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert "message" in message


def test_delete_does_not_exist(
    client: TestClient, random_dnd_class: schemas.DndClassCreate
) -> None:
    """Test delete: 404."""
    random_dnd_class_copy = schemas.DndClassCreate(**random_dnd_class.dict())
    random_dnd_class_copy.id = -999999999
    response = client.delete(
        f"{settings.API_V1_STR}/classes?id={random_dnd_class_copy.id}"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("count", range(2))
def test_post_bulk(client: TestClient, test_data_directory: str, count) -> None:
    """Test /bulk post: happy path -> runs twice to test idempotence."""
    assert count is not None, "avoiding W0613: unused-argument"
    files = {
        "upload_file": (
            "class.json",
            open(f"{test_data_directory}/json/seeds/class.json", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{settings.API_V1_STR}/classes/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    bulk_load_response = schemas.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored == 0


def test_post_bulk_bad_filetype(client: TestClient, test_data_directory: str) -> None:
    """Test /bulk post: illegal file type (foo/bar)."""
    files = {
        "upload_file": (
            "class.json",
            open(f"{test_data_directory}/json/seeds/class.json", "rb"),
            "foo/bar",
        )
    }
    response = client.post(
        f"{settings.API_V1_STR}/classes/bulk",
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
        f"{settings.API_V1_STR}/classes/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    bulk_load_response = schemas.BulkLoadResponse(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert bulk_load_response.totals.errored > 0


def test_clean_up(client: TestClient, db: Session) -> None:
    """Remove anything added from this test file: [classes, sources]."""
    # clean up classes
    db.query(models.DndClass).delete()
    db.commit()
    response = client.get(f"{settings.API_V1_STR}/classes")
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_json.get("data")) == 0
    # clean up sources
    db.query(models.Source).delete()
    db.commit()
    response = client.get(f"{settings.API_V1_STR}/sources")
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(response_json.get("data")) == 0
