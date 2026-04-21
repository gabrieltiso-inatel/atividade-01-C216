from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ping successfull"}


def test_query_param():
    response = client.get("/api/v1/hello?name=Gabriel&age=22")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Gabriel, you are 22 years old"}


def test_path_param():
    response = client.get("/api/v1/hello/Gabriel/22")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Gabriel, you are 22 years old"}


def test_post():
    response = client.post(
        "/api/v1/hello",
        json={"name": "Gabriel", "age": 22}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Gabriel, you are 22 years old"}

def test_post_invalid():
    response = client.post("/api/v1/hello", json={})
    assert response.status_code == 422

def test_put():
    response = client.put(
        "/api/v1/update",
        json={"name": "Gabriel", "age": 22}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso atualizado com o nome: Gabriel, idade 23"}


def test_delete():
    response = client.delete("/api/v1/delete?name=Gabriel&age=22")
    assert response.status_code == 200
    assert response.json() == {"message": "Recurso deletado com o nome: Gabriel, idade 22"}


def test_patch():
    response = client.patch(
        "/api/v1/patch",
        json={"name": "Gabriel", "age": 22}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Modificação parcial aplicada ao recurso com o nome: Gabriel, idade 22"}