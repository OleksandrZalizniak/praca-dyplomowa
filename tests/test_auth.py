import json
import pytest
from app import create_app, db


def test_register_and_login(client):
    response = client.post(
        "/register",
        json={"username": "test", "password": "test123"}
    )
    assert response.status_code == 201

    response = client.post(
        "/login",
        json={"username": "test", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.get_json()



