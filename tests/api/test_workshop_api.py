from fastapi.testclient import TestClient
from app.main import create_app
import tempfile
import os
import pytest
from app import database
from pathlib import Path

@pytest.fixture
def database_path():
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
    db_path_str = db_file.name
    db_file.close()
    db_path = Path(db_path_str)
    database.initialize(db_path)
    yield db_path
    os.unlink(db_path)

@pytest.fixture
def client(database_path):
    app = create_app(database_path=database_path)
    return TestClient(app)

# PDF A：复制的标准测试
def test_post_car_returns_201_and_json(client):
    payload = {"make": "Ford", "model": "Fiesta", "year": 2018, "color": "Black"}
    response = client.post("/api/cars", json=payload)
    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

# PDF D：自己写的用例：非法年份1800，返回422，数据库不保存
def test_invalid_year_is_not_saved(client):
    payload = {"make": "Honda", "model": "Civic", "year": 1800, "color": "Red"}
    resp_post = client.post("/api/cars", json=payload)
    assert resp_post.status_code == 422

    resp_get = client.get("/api/cars")
    data_list = resp_get.json()
    assert data_list == []