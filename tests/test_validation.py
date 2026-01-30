import pytest
import json
from app import create_app, db


def test_register_no_json(client):
    response = client.post("/register")
    assert response.status_code == 400


def test_register_empty_fields(client):
    response = client.post(
        "/register",
        json={"username": "", "password": ""}
    )
    assert response.status_code == 400


def test_register_short_password(client):
    response = client.post(
        "/register",
        json={"username": "test2", "password": "123"}
    )
    assert response.status_code == 400


def test_register_valid_data(client):
    response = client.post(
        "/register",
        json={"username": "validuser", "password": "strongpass"}
    )
    assert response.status_code == 201

