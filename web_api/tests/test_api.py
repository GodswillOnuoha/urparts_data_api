from fastapi.testclient import TestClient

from app import api

client = TestClient(api)


def test_read_default():
    response = client.get("/api/parts")
    data = response.json()

    assert response.status_code == 200
    assert list(data[0].keys()) == [
        "id",
        "model_id",
        "part_number",
        "category",
        "manufacturer",
        "machine_type",
        "machine_model",
    ]


def test_read_param_limit():
    response = client.get("/api/parts?limit=2")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


def test_filter_part_number():
    response = client.get("/api/parts?part_number=ND050477&limit=1")
    data = response.json()
    assert data[0]["part_number"] == "ND050477"


def test_filter_category():
    response = client.get("/api/parts?category=RIGHT UPHOLSTERING&limit=1")
    data = response.json()
    assert data[0]["category"] == "RIGHT UPHOLSTERING"


def test_filter_manufacturer():
    response = client.get("/api/parts?manufacturer=Volvo&limit=1")
    data = response.json()
    assert data[0]["manufacturer"] == "Volvo"
