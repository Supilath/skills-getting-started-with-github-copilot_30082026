from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    response = client.post("/activities/Chess Club/signup?email=student@example.com")
    assert response.status_code == 200

    response = client.post("/activities/Chess Club/signup?email=student@example.com")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity():
    client.post("/activities/Chess Club/signup?email=remove-me@example.com")

    response = client.delete("/activities/Chess Club/signup?email=remove-me@example.com")

    assert response.status_code == 200
    assert response.json()["message"] == "Removed remove-me@example.com from Chess Club"

    activity = client.get("/activities").json()["Chess Club"]
    assert "remove-me@example.com" not in activity["participants"]
