from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Reset database before running tests"""
    client.delete("/api/v1/alunos/")
    yield
    # Cleanup after all tests
    client.delete("/api/v1/alunos/")


class TestStudentCreation:
    def test_create_first_ges_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "Alice Silva",
            "email": "alice@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES1"
        assert data["name"] == "Alice Silva"
        assert data["course"] == "GES"
        assert data["registration"] == 1

    def test_create_second_ges_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "Bob Santos",
            "email": "bob@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES2"
        assert data["registration"] == 2

    def test_create_third_ges_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "Carol Oliveira",
            "email": "carol@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES3"
        assert data["registration"] == 3

    def test_create_first_gec_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "David Teixeira",
            "email": "david@example.com",
            "course": "GEC"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GEC1"
        assert data["course"] == "GEC"
        assert data["registration"] == 1

    def test_create_second_gec_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "Eva Marques",
            "email": "eva@example.com",
            "course": "GEC"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GEC2"
        assert data["registration"] == 2

    def test_create_third_gec_student(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "Frank Cardoso",
            "email": "frank@example.com",
            "course": "GEC"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GEC3"
        assert data["registration"] == 3


class TestStudentListing:
    def test_list_all_students(self):
        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        students = response.json()
        assert len(students) == 6
        courses = [s["course"] for s in students]
        assert courses.count("GES") == 3
        assert courses.count("GEC") == 3


class TestStudentRetrieval:
    def test_find_existing_ges_student(self):
        response = client.get("/api/v1/alunos/GES1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES1"
        assert data["name"] == "Alice Silva"

    def test_find_existing_gec_student(self):
        response = client.get("/api/v1/alunos/GEC2")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GEC2"
        assert data["name"] == "Eva Marques"

    def test_find_nonexistent_student_returns_404(self):
        response = client.get("/api/v1/alunos/NONEXISTENT")
        assert response.status_code == 404


class TestStudentUpdate:
    def test_update_student_name_and_email(self):
        response = client.patch("/api/v1/alunos/GES1", json={
            "name": "Alice Silva Updated",
            "email": "alice.updated@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES1"
        assert data["name"] == "Alice Silva Updated"
        assert data["email"] == "alice.updated@example.com"

    def test_update_nonexistent_student_returns_404(self):
        response = client.patch("/api/v1/alunos/NONEXISTENT", json={
            "name": "Nonexistent",
            "email": "nonexistent@example.com",
            "course": "GES"
        })
        assert response.status_code == 404


class TestStudentDeletion:
    def test_delete_ges_student(self):
        response = client.delete("/api/v1/alunos/GES3")
        assert response.status_code == 200
        assert response.json()["message"] == "Student deleted successfully"

    def test_deleted_student_cannot_be_found(self):
        response = client.get("/api/v1/alunos/GES3")
        assert response.status_code == 404

    def test_new_student_in_same_course_gets_new_id(self):
        response = client.post("/api/v1/alunos/", json={
            "name": "George Mendes",
            "email": "george@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "GES4"


class TestDataPersistence:
    def test_data_persists_across_connections(self):
        """Verify that data created in earlier tests still exists"""
        # Create a new student
        response = client.post("/api/v1/alunos/", json={
            "name": "Helen Lima",
            "email": "helen@example.com",
            "course": "GES"
        })
        assert response.status_code == 200
        student_id = response.json()["id"]

        # Retrieve it to verify persistence
        response = client.get(f"/api/v1/alunos/{student_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Helen Lima"

        # List all and verify the new student is there
        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        student_ids = [s["id"] for s in response.json()]
        assert student_id in student_ids

    def test_deleted_id_is_not_reused(self):
        response = client.get("/api/v1/alunos/GES3")
        assert response.status_code == 404

    def test_delete_nonexistent_student_returns_404(self):
        response = client.delete("/api/v1/alunos/NONEXISTENT")
        assert response.status_code == 404


class TestStudentReset:
    def test_reset_all_students(self):
        response = client.delete("/api/v1/alunos/")
        assert response.status_code == 200
        assert response.json()["message"] == "All students have been deleted"

    def test_list_is_empty_after_reset(self):
        response = client.get("/api/v1/alunos/")
        assert response.status_code == 200
        assert response.json() == []


class TestRoot:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "API working 🚀"