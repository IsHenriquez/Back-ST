import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, engine

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_vehicle(test_db):
    data = {
        "id_vehicle_model": 1,
        "is_busy": False,
        "active": 1,
        "plate": "ABC123",
        "description": "Vehículo prueba"
    }
    response = client.post("/vehicles/", json=data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["plate"] == data["plate"]
    assert "id" in json_response

def test_read_vehicles(test_db):
    response = client.get("/vehicles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_vehicle_by_id(test_db):
    data = {"id_vehicle_model": 1}
    create_response = client.post("/vehicles/", json=data)
    vehicle_id = create_response.json()["id"]

    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200
    assert response.json()["id"] == vehicle_id

def test_update_vehicle(test_db):
    data = {"id_vehicle_model": 1}
    create_response = client.post("/vehicles/", json=data)
    vehicle_id = create_response.json()["id"]

    update_data = {"plate": "XYZ789"}
    response = client.put(f"/vehicles/{vehicle_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["plate"] == update_data["plate"]

def test_delete_vehicle(test_db):
    data = {"id_vehicle_model": 1}
    create_response = client.post("/vehicles/", json=data)
    vehicle_id = create_response.json()["id"]

    response = client.delete(f"/vehicles/{vehicle_id}")
    assert response.status_code == 200

    response = client.get(f"/vehicles/{vehicle_id}")
    assert response.status_code == 404