import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data  # Should not be empty

def test_signup_and_prevent_duplicate():
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Second signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json().get("detail", "")

def test_signup_invalid_activity():
    resp = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404

def test_participants_listed():
    activity = list(client.get("/activities").json().keys())[0]
    email = "listuser@example.com"
    client.post(f"/activities/{activity}/signup?email={email}")
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
