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


def test_get_character_by_id(client):
    pass


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

