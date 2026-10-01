from fastapi.testclient import TestClient
from app.main import app

def test_homepage():
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert "ComicCraft" in response.text
