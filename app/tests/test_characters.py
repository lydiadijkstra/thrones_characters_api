import pytest
from bson import ObjectId
from app.main import app
from app.core.database import characters_collection  # Import the MongoDB collection


@pytest.fixture()
def client():
    """
    Fixture to create a test client for running simulated HTTP requests to the Flask app.
    """
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture()
def test_character():
    """
    Fixture to insert a test character into the database before tests.
    This ensures that we have a known character to test retrieval, updates, and deletion.
    """
    character_data = {
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
    inserted_character = characters_collection.insert_one(character_data)
    character_data["_id"] = str(inserted_character.inserted_id)  # Convert ObjectId to string
    yield character_data  # Provide the character for tests
    characters_collection.delete_one({"_id": ObjectId(inserted_character.inserted_id)})  # Cleanup


def test_not_found(client):
    """
    Test case for a non-existent endpoint.
    """
    response = client.get("/wrong_endpoint")
    assert response.status_code == 404


def test_get_character_by_id(client, test_character):
    """
    Test fetching a character by its MongoDB ID.
    """
    character_id = test_character["_id"]

    response = client.get(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json["_id"] == character_id
    assert response.json["name"] == "Jon Snow"


def test_get_characters(client):
    """
    Test fetching the list of characters with pagination.
    """
    response = client.get("/characters/")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) >= 1  # At least one character should exist


def test_add_character(client):
    """
    Test adding a new character.
    """
    new_character = {
        "name": "Mock Data",
        "house": "Mock House",
        "animal": "Mock Animal",
        "symbol": "Mock Symbol",
        "nickname": "Mock Nickname",
        "role": "Mock role",
        "age": 25,
        "death": None,
        "strength": "Mock Strength"
    }
    response = client.post("/characters/", json=new_character)
    assert response.status_code == 201

    created_character = response.json["created_character"]
    assert created_character["name"] == "Mock Data"
    assert "_id" in created_character  # MongoDB should assign an _id


def test_edit_character(client, test_character):
    """
    Test editing an existing character.
    """
    character_id = test_character["_id"]

    updated_data = {"age": 30, "nickname": "The White Wolf"}
    response = client.patch(f"/characters/{character_id}", json=updated_data)

    assert response.status_code == 200
    assert response.json["updated_character"]["age"] == 30
    assert response.json["updated_character"]["nickname"] == "The White Wolf"


def test_delete_character(client, test_character):
    """
    Test deleting a character.
    """
    character_id = test_character["_id"]

    response = client.delete(f"/characters/{character_id}")
    assert response.status_code == 200
    assert response.json["message"] == "Character deleted successfully!"

    # Ensure it's actually deleted
    response_check = client.get(f"/characters/{character_id}")
    assert response_check.status_code == 404
