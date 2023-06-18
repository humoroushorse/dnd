"""Helper functions for integration tests."""
from typing import Type, TypeVar

from dnd import schemas
from dnd.core import uncached_settings
from dnd.database.base_class import Base
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


def purge_table(
    client: TestClient, db: Session, model: Type[ModelType], endpoint: str
) -> None:
    """Completely purge a table and then check that nothing exists at the endpoint."""
    db.query(model).delete()
    db.commit()
    response = client.get(f"{uncached_settings.API_V1_STR}/{endpoint}")
    assert (
        response.status_code == status.HTTP_200_OK
    ), f"expected clean deletions for /{endpoint}"
    response_json = schemas.responses.GenericListResponse(**response.json())
    assert len(response_json.data) == 0, f"expected no data remaining for /{endpoint}"


def bulk_load_file(client: TestClient, test_data_path: str, endpoint: str) -> None:
    """Bulk load data for a given endpoint and verify no errors."""
    file_name = test_data_path.rsplit("/", 1)[-1]
    files = {
        "upload_file": (
            file_name,
            open(f"{test_data_path}", "rb"),
            "application/json",
        )
    }
    response = client.post(
        f"{uncached_settings.API_V1_STR}/{endpoint}/bulk",
        files=files,
        headers={"accept": "application/json"},
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = schemas.responses.BulkLoadResponse(**response.json())
    assert response_json.totals.errored == 0
