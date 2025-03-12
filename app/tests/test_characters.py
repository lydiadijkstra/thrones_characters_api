import pytest
from app.main import app, characters_collection  # Import Flask app & MongoDB

@pytest.fixture
def client():
    """Creates a test client for Flask."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_character():
    """Fixture for a test character added to MongoDB."""
    test_char = {
        "id": 999,
        "name": "Test Character",
        "house": "Test House",
        "animal": "Test Animal",
        "symbol": "Test Symbol",
        "nickname": "Test Nickname",
        "role": "Test Role",
        "age": 30,
        "death": None,
        "strength": "Test Strength"
    }
    characters_collection.insert_one(test_char)
    yield test_char
    characters_collection.delete_one({"id": 999})  # Cleanup


def test_get_characters(client):
    """Test fetching the list of characters."""
    response = client.get("/characters/")
    assert response.status_code == 200
    assert "characters" in response.json
    assert isinstance(response.json["characters"], list)


def test_get_character_by_id(client, test_character):
    """Test fetching a single character by ID."""
    response = client.get(f"/characters/{test_character['id']}")
    assert response.status_code == 200
    assert response.json["name"] == "Test Character"


def test_add_character(client):
    """Test adding a new character."""
    new_character = {
        "name": "New Character",
        "house": "New House",
        "animal": "New Animal",
        "symbol": "New Symbol",
        "nickname": "New Nickname",
        "role": "New Role",
        "age": 25,
        "death": None,
        "strength": "New Strength"
    }
    response = client.post("/characters/", json=new_character)
    assert response.status_code == 201
    assert "created_character" in response.json
    characters_collection.delete_one({"name": "New Character"})  # Cleanup


def test_edit_character(client, test_character):
    """Test editing an existing character."""
    updated_data = {"age": 35, "nickname": "Updated Nickname"}
    response = client.patch(f"/characters/{test_character['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json["updated_character"]["age"] == 35
    assert response.json["updated_character"]["nickname"] == "Updated Nickname"


def test_delete_character(client, test_character):
    """Test deleting a character."""
    response = client.delete(f"/characters/{test_character['id']}")
    assert response.status_code == 200
    assert response.json["message"] == "Character deleted successfully!"
    assert characters_collection.find_one({"id": test_character["id"]}) is None
