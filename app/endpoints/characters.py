# Flask imports
from flask import Blueprint, jsonify, request

# Random
from random import sample

# imports
from app.data.json_data_fetcher import fetch_data
from app.storage.store_json import save_data
from app.endpoints.functions import filtering, sorting
from app.storage.database import characters_collection


# Blueprint for possibility to have several endpoints
characters_bp = Blueprint("characters", __name__, url_prefix="/characters")


def get_character_by_id(id):
    """
    Helper Function to fetch character by ID, usage in several routes
    :param id: character ID
    :return: character belonging to the ID
    """
    characters = fetch_data()

    # Loop through the list to find the matching character_id
    for character in characters:
        if character["id"] == id:
            return character
    return None


@characters_bp.route("/", methods=["GET"])
@characters_bp.route("/filter", methods=["GET"])
def get_characters():
    """
    Fetch characters with optional filtering, sorting, pagination, and random selection
    :return: Paginated list of characters
    """
    #characters = fetch_data()
    characters = list(characters_collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id`

    # Apply filtering
    filtered_characters = filtering(characters)

    # Apply sorting
    sorted_characters = sorting(filtered_characters)

    # Use slicing to slice from the number to skip until the limit, default limit 20
    limit = request.args.get("limit", default=20, type=int)
    skip = request.args.get("skip", default=0, type=int)

    # Pick a number of characters randomly from the list
    if "limit" not in request.args and "skip" not in request.args and "sort_by" not in request.args:
        random_choice_of_characters = sample(sorted_characters, min(limit, len(sorted_characters)))
        return jsonify({
            "characters": random_choice_of_characters
        })

    # Paginate the list of characters
    paginated_characters = sorted_characters[skip : skip + limit]
    return jsonify({
        "message": "Characters fetched successfully!",
        "characters": paginated_characters
    }), 200


@characters_bp.route("/<int:id>", methods=["GET"])
def display_character_by_id(id):
    """
    Endpoint for fetching data for character with the matching id
    :param id:
    :return: json data of the character that fits the id
    """
    character = get_character_by_id(id)
    print(character)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character)


@characters_bp.route("/", methods=["POST"])
def add_character():
    """
    Endpoint for adding a new character
    :param id: all data for creating new character
    :return: json data of new character
    """
    #characters = fetch_data()

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Auto Increment ID logic by finding last DB-character + 1
    last_character = characters_collection.find_one(sort=[("id", -1)])
    new_id = 1 if last_character is None else last_character["id"] + 1

    new_character = {
        "id": new_id,
        "name": data["name"],
        "house": data["house"],
        "animal": data["animal"],
        "symbol": data["symbol"],
        "nickname": data["nickname"],
        "role": data["role"],
        "age": data["age"],
        "death": data["death"],
        "strength": data["strength"],
    }

    characters_collection.insert_one(new_character)
    del new_character["_id"]

    return jsonify({
        "message": "Character added successfully!",
        "created_character": new_character
    }), 201


@characters_bp.route("/<int:id>", methods=["PATCH"])
def edit_character(id):
    """
    Endpoint for updating character data
    """
    characters = fetch_data()

    character = get_character_by_id(id)

    if not character:
        return jsonify({"error": "Character not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    character.update(data)

    save_data(characters)

    return jsonify({
        "message": "Character updated successfully!",
        "updated_character": character
    })


@characters_bp.route("/<int:id>", methods=["DELETE"])
def delete_character(id):
    """
    Endpoint for deleting a character on behalf of the id
    :param id: ID of the character which should be deleted
    :return: List with chracters without the deleted character
    """
    characters = fetch_data()

    character = get_character_by_id(id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    characters.remove(character)
    save_data(characters)

    return jsonify({"message": "Character deleted successfully!"})
