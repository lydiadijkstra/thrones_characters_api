import pytest

from app.endpoints.characters import get_characters_data, get_character_by_id
from app.main import app


@pytest.fixture()
def client():
    """
    Fixture to create a test client for running simulated HTTP requests to the Flask app.
    The client allows us to interact with the API without running the actual Flask server.
    :return: Flask test client
    """
    app.testing = True
    with app.test_client() as client:
        yield client


def test_not_found(client):
    """
    Test case for a non-existent endpoint.
    This ensures that a request to an invalid endpoint returns a 404 status code.
    :param client: The Flask test client
    :return: None
    """
    response = client.get("/wrong_endpoint")
    assert response.status_code == 404


def test_get_character_by_id(client):
    """
    Test case for fetching a character by its ID using the helper function.
    It tests both valid and invalid IDs to ensure proper handling.
    :param client: The Flask test client
    :return: None
    """
    assert get_character_by_id(1) == {
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

    # Number out of range
    assert get_character_by_id(999) == None
    assert get_character_by_id(0) == None
    assert get_character_by_id(-1) == None # Negative number
    assert get_character_by_id(6.6) == None # Entering a float
    assert get_character_by_id("string") == None # Entering a string


def test_get_characters_data(client):
    """
    Test case for fetching the list of characters with pagination.
    This tests various combinations of the pagination parameters (limit and skip).
    :param client: The Flask test client
    :return: None
    """
    # Test default 20 characters
    response = client.get("/characters/")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) <= 20

    # Test pagination, limit = 5, skip = 0
    response_set_limit_and_skip = client.get("/characters/?limit=2&skip=0")
    assert response_set_limit_and_skip.status_code == 200
    assert len(response_set_limit_and_skip.json) <= 2

    # Test pagination, limit = 10, skip = 5
    response_set_limit_10 = client.get("/characters/?limit=10&skip=5")
    assert response_set_limit_10.status_code == 200
    assert len(response_set_limit_10.json) <= 10

    # Test pagination, limit exceeds number of characters
    response_limit_exceeds_characters = client.get("/characters/?limit=999")
    assert response_limit_exceeds_characters.status_code == 200
    assert len(response_limit_exceeds_characters.json) <= 999

    # Test pagination, limit set to zero
    response_set_limit_zero = client.get("/characters/?limit=0")
    assert response_set_limit_zero.status_code == 200
    assert isinstance(response_set_limit_zero.json, list)
    assert len(response_set_limit_zero.json) == 0


def test_display_character_by_id(client):
    """
    Test case for fetching a character by ID using the /characters/{id} endpoint.
    It tests valid and invalid IDs (including negative numbers, non-existent, and non-numeric IDs).
    :param client: The Flask test client
    :return: None
    """
    #testing correct id-nr
    response = client.get("/characters/1")

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

    # Testing negativ id-nr.
    negative_nr_response = client.get("/characters/-1")
    assert negative_nr_response.status_code == 404

    # Testing id-nr. out of range
    nr_out_of_range_response = client.get("/characters/999")
    assert nr_out_of_range_response.json == {"error":"Character not found"}

    # Testing id-nr. with zero
    nr_zero_response = client.get("/characters/0")
    assert nr_zero_response.json == {"error": "Character not found"}

    # Testing id-nr. with a float
    nr_is_float_response = client.get("/characters/6.6")
    assert nr_is_float_response.json == {"error": "Character not found"}

    # Testing id-nr. with a string
    entering_string_response = client.get("/characters/'string'")
    assert entering_string_response.json == {"error": "Character not found"}


def test_add_character(client):
    """
    Test case for adding a new character using the /characters/ POST endpoint.
    It ensures that the new character is successfully added and returned with correct data.
    :param client: The Flask test client
    :return: None
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
    assert response.json == {'created_character':
        {
            "id": 51,
            "name": "Mock Data",
            "house": "Mock House",
            "animal": "Mock Animal",
            "symbol": "Mock Symbol",
            "nickname": "Mock Nickname",
            "role": "Mock role",
            "age": 25,
            "death": None,
            "strength": "Mock Strength"
        }, 'message': 'Character added successfully!',
    }


def test_edit_character(client):
    """
    Test case for editing an existing character using the /characters/{id} PATCH endpoint.
    It ensures that a character's details can be successfully updated.
    :param client: The Flask test client
    :return: None
    """
    # Updating all data of a character
    editing_character = {
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

    response = client.patch("/characters/1", json=editing_character)

    assert response.status_code == 200
    assert response.json == {
        'message': 'Character updated successfully!',
            'updated_character': {
            "id": 1,
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
    }

    # Updating partial character
    editing_character = {
        "house": "Mock House",
        "animal": "Mock Animal",
        "symbol": "Mock Symbol",
        "nickname": "Mock Nickname",
        "age": 100,
        "strength": "Mock Strength"
    }

    response = client.patch("/characters/1", json=editing_character)

    assert response.status_code == 200
    assert response.json == {
        'message': 'Character updated successfully!',
        'updated_character': {
            "id": 1,
            "name": "Jon Snow",
            "house": "Mock House",
            "animal": "Mock Animal",
            "symbol": "Mock Symbol",
            "nickname": "Mock Nickname",
            "role": "King",
            "age": 100,
            "death": None,
            "strength": "Mock Strength"
        }
    }


def test_delete_character(client):
    """
    Testing editing a character - endpoint
    :param client:
    :return:
    """
    response = client.delete("/characters/1")

    assert response.status_code == 200
    assert response.json == {
        'message': 'Character deleted successfully!'
    }
