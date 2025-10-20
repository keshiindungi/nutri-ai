# backend/tests/test_api.py
from fastapi.testclient import TestClient
from backend.main import app 

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_recommend_basic():
    payload = {
        "age": 30,
        "sex": "female",
        "height_cm": 165,
        "weight_kg": 65,
        "activity_level": "moderate",
        "goal": "maintain",
        "diet": "omnivore",
        "allergies": [],
        "daily_budget_ksh": 300,
        "preferred_cuisines": []
    }
    r = client.post("/api/recommend/", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "daily_calorie_target" in body
    assert "recommendations" in body
