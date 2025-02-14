import json

import pytest
from app.main import app


@pytest.fixture()
def client():
    """
    Create client to run tests with simulated HTTP requests to the API without running the FLASK application
    :return:
    """
    app.testing = True
    with app.test_client() as client:
        yield client

def test_not_found(client):
    response = client.get("/wrong_endpoint")
    assert response.status_code == 404


def test_get_character_by_id(client):
    response = client.get("/characters/1")

    print("Response status: ", response.status_code)
    print("Response JSON: ", response.json)

    assert response.status_code == 200
    assert response.json == {
    "id": 1,
    "name": "Jon Snow",
    "house": "Stark",
    "animal": "Direwolf",
    "symbol": "Wolf",
    "nickname": "King in the North",
    "role": "King",
    "age": 25,
    "death": None,
    "strength": "Physically strong"
  }

def test_get_characters_data(client):
    pass


def test_display_character_by_id(client):
    pass


def test_add_character(client):
    pass


def test_edit_character(client):
    pass


def test_delete_character(client):
    pass

