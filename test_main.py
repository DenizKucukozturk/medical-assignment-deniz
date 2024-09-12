from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_procedure_info_from_collector__happy_path():
    collector_id = 1567
    response = client.get(f"/collectors/{collector_id}/procedure-info")

    assert response.status_code == 200
    assert response.json() == {
        "procedure": {
            "id": 1,
            "subject": {
                "id": 1
            },
        }
    }


def test_get_procedure_info_from_collector__procedure_not_found():
    collector_id = 1
    response = client.get(f"/collectors/{collector_id}/procedure-info")

    assert response.status_code == 404
    assert response.json() == {"detail": "Procedure not found"}


def test_get_procedure_info_from_collector__invalid_input():
    collector_id = "a"
    response = client.get(f"/collectors/{collector_id}/procedure-info")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": collector_id,
                "loc": ["path", "tube_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                'type': 'int_parsing'
            }
        ]
    }


def test_get_collection_info__happy_path():
    procedure_id = 1
    response = client.get(f"/procedures/{procedure_id}/collection-info")

    assert response.status_code == 200
    assert response.json() == {
        "procedure": {
            "id": 1,
            "subject": {
                "id": 1
            },
            "collection_result": "success",
            "collectors": [
                {
                    "id": 1567,
                    "sequence": 1,
                    "collection_result": "filled",
                },
                {
                    "id": 1568,
                    "sequence": 2,
                    "collection_result": "filled",
                },
                {
                    "id": 1569,
                    "sequence": 3,
                    "collection_result": "filled",
                }
            ]
        }
    }


def test_get_collection_info__procedure_not_found():
    procedure_id = 123
    response = client.get(f"/procedures/{procedure_id}/collection-info")

    assert response.status_code == 404
    assert response.json() == {"detail": "Procedure not found"}


def test_get_collection_info__invalid_input():
    procedure_id = "a"
    response = client.get(f"/procedures/{procedure_id}/collection-info")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": procedure_id,
                "loc": ["path", "procedure_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                'type': 'int_parsing'
            }
        ]
    }


def test_patch_procedure_collection_info__happy_path():
    procedure_input = {
        "collection_result": "partial_success",
        "collectors": [
            {
                "id": 203948,
                "sequence": 1,
                "collection_result": "filled"
            },
            {
                "id": 2352,
                "sequence": 2,
                "collection_result": "partial_filled"
            }
        ]
    }

    procedure_id = 1
    response = client.patch(
        f"/procedures/{procedure_id}/collection-info",
        json={"procedure": procedure_input}
    )

    assert response.status_code == 200

    updated_procedure = response.json()["procedure"]

    assert updated_procedure["collection_result"] == procedure_input["collection_result"]
    assert updated_procedure["collectors"] == procedure_input["collectors"]


def test_patch_procedure_collection_info__procedure_not_found():
    procedure_input = {
        "collection_result": "partial_success",
        "collectors": [
            {
                "id": 203948,
                "sequence": 1,
                "collection_result": "filled"
            },
            {
                "id": 2352,
                "sequence": 2,
                "collection_result": "partial_filled"
            }
        ]
    }

    procedure_id = 999
    response = client.patch(
        f"/procedures/{procedure_id}/collection-info",
        json={"procedure": procedure_input}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Procedure not found"}


def test_patch_procedure_collection_info__extra_input_field():
    procedure_input = {
        "id": 12,
        "collection_result": "partial_success",
        "collectors": [
            {
                "id": 203948,
                "sequence": 1,
                "collection_result": "filled"
            },
            {
                "id": 2352,
                "sequence": 2,
                "collection_result": "partial_filled"
            }
        ]
    }

    procedure_id = 1
    response = client.patch(
        f"/procedures/{procedure_id}/collection-info",
        json={
            "procedure": procedure_input
        }
    )

    assert response.status_code == 422
    assert response.json() == {
        'detail':
            [
                {
                    'input': 12,
                    'loc': ['body', 'procedure', 'id'],
                    'msg': 'Extra inputs are not permitted',
                    'type': 'extra_forbidden'
                }
            ]
    }
