import http

import pytest

from fastapi.testclient import TestClient

from cleanerrobot.main import app

unprocessable_json_data_provider = [
    [
        {
            "start": {"x": 0, "y": -120_000},
            "commands": [
                {"direction": "north", "steps": 1},
            ]
        }
    ],
    [
        {
            "start": {"x": 0, "y": 120_000},
            "commands": [
                {"direction": "north", "steps": 1},
            ]
        }
    ],
    {
        "start": {"x": 100_010, "y": 0},
        "commands": [
            {"direction": "north", "steps": 1},
        ]
    },
    {
        "start": {"x": -100_010, "y": 0},
        "commands": [
            {"direction": "north", "steps": 1},
        ]
    },
    {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "northeast", "steps": 1},
        ]
    },
    {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "north", "steps": 0},
        ]
    },
    {
        "start": {"x": 0, "y": 0},
        "commands": [
            {"direction": "north", "steps": 100_000},
        ]
    }
]


@pytest.fixture
def test_client(db_engine):
    return TestClient(app)


@pytest.mark.parametrize("json", unprocessable_json_data_provider)
def test_schema_parameters(test_client, json):
    response = test_client.post(
        "/tibber-developer-test/enter-path",
        json=json
    )

    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


def test_request_successul_clean_command(test_client):
    response = test_client.post(
        "/tibber-developer-test/enter-path?size=10",
        json={
            "start": {"x": 0, "y": 0},
            "commands": [
                {"direction": "north", "steps": 2},
                {"direction": "east", "steps": 1},
            ]
        }
    )

    expected_json = {
        "id": 1,
        "commands": 2,
        "result": 4,
        "duration": 0.0000123,
        "timestamp": "2023-11-05T15:01:39.852682Z"
    }

    actual_json = response.json()

    assert response.status_code == http.HTTPStatus.CREATED
    assert actual_json.get("id") == expected_json.get("id")
    assert actual_json.get("commands") == expected_json.get("commands")
    assert actual_json.get("result") == expected_json.get("result")
    assert actual_json.get("duration") > 0.0
