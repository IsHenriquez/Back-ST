import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, engine, SessionLocal

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_ticket(test_db):
    data = {
        "title": "Test Ticket",
        "description": "Descripción de prueba",
        "address": "Calle Falsa 123",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = client.post("/tickets/", json=data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["title"] == data["title"]
    assert "id" in json_response

def test_read_tickets(test_db):
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_ticket_by_id(test_db):
    # Crear ticket para obtener id
    data = {"title": "Ticket para leer"}
    create_response = client.post("/tickets/", json=data)
    ticket_id = create_response.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ticket_id

def test_update_ticket(test_db):
    # Crear ticket para actualizar
    data = {"title": "Antes update"}
    create_response = client.post("/tickets/", json=data)
    ticket_id = create_response.json()["id"]

    update_data = {"title": "Después update"}
    response = client.put(f"/tickets/{ticket_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

def test_delete_ticket(test_db):
    # Crear ticket para borrar
    data = {"title": "Para borrar"}
    create_response = client.post("/tickets/", json=data)
    ticket_id = create_response.json()["id"]

    response = client.delete(f"/tickets/{ticket_id}")
    assert response.status_code == 200

    # Confirmar que ya no existe
    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code == 404
