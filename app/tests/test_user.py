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

def test_create_user(test_db):
    data = {
        "name": "John",
        "password": "mypassword",
        "email": "john@example.com",
        "active": True
    }
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["name"] == data["name"]
    assert "id" in json_response

def test_read_users(test_db):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_user_by_id(test_db):
    data = {"name": "Alice", "password": "pass123"}
    create_response = client.post("/users/", json=data)
    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_update_user(test_db):
    data = {"name": "Bob", "password": "oldpass"}
    create_response = client.post("/users/", json=data)
    user_id = create_response.json()["id"]

    update_data = {"name": "BobUpdated", "password": "newpass"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_user(test_db):
    data = {"name": "ToDelete", "password": "delpass"}
    create_response = client.post("/users/", json=data)
    user_id = create_response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
