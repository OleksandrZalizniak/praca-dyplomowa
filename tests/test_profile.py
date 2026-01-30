import json
import pytest
from app import create_app, db

def register_and_login(client):
    client.post(
        "/register",
        json={"username": "test", "password": "test123"}
    )

    response = client.post(
        "/login",
        json={"username": "test", "password": "test123"}
    )

    return response.get_json()["access_token"]


def test_profile_without_jwt(client):
    response = client.get("/profile")
    assert response.status_code == 401


def test_profile_with_jwt(client):
    token = register_and_login(client)

    response = client.get(
        "/profile",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Access granted"
    assert data["user"] == "test"

