# Flask imports
from flask import Blueprint, jsonify, request

# Random
from random import sample

# imports
from app.data.json_data_fetcher import fetch_data
from app.storage.store_json import save_data


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
def get_characters_data():
    """
    Endpoint for fetching characters from the JSON file with pagination
    :return: Paginated list of characters
    """
    characters = fetch_data()

    # Use slicing to slice from the number to skip until the limit, default limit 20
    limit = request.args.get("limit", default=20, type=int)
    skip = request.args.get("skip", default=0, type=int)

    # Pick a number of characters randomly from the list
    if limit and skip == 0:
        random_choice_of_characters = sample(characters, min(limit, len(characters)))
    else:
        # Paginate the list of characters
        paginated_characters = characters[skip : skip + limit]
        return paginated_characters
    return jsonify(random_choice_of_characters)


@characters_bp.route("/<int:id>", methods=["GET"])
def display_character_by_id(id):
    """
    Endpoint for fetching data for character with the matching id
    :param id:
    :return: json data of the character that fits the id
    """
    character = get_character_by_id(id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character)



@characters_bp.route("/", methods=["POST"])
def add_character(id, name, house, animal, symbol, nickname, role, age, death, strength):
    """
    Endpoint for adding a new character
    :param id: all data for creating new character
    :return: json data of new character
    """
    characters = fetch_data()

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_character = {
        "id": len(characters) + 1,
        "name": data["name"],
        "house": data["house"],
        "animal": data["animal"],
        "symbol": data["symbol"],
        "nickname": data["nickname"],
        "role": data["role"],
        "age": data["age"],
        "death": data["death"],
        "strength": data["strength"]
    }

    characters.append(new_character)
    save_data(characters)

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
    :param id:
    :return:
    """
    characters = fetch_data()

    character = get_character_by_id(id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    characters.remove(character)
    save_data(characters)

    return jsonify({"message": "Character deleted successfully!"})

