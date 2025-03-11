# Flask imports
from flask import Blueprint, jsonify, request
from random import sample
from pymongo import MongoClient
from app.endpoints.functions import filtering, sorting

client = MongoClient("mongodb://localhost:27017/")
db = client["thrones_db"]
characters_collection = db["characters"]

# Blueprint for API-Endpoints
characters_bp = Blueprint("characters", __name__, url_prefix="/characters")


def get_character_by_id(character_id):
    """
    Holt einen Charakter anhand der ID aus MongoDB.
    :param character_id: ID des Charakters
    :return: Dikt-Objekt des Charakters oder None, falls nicht gefunden
    """
    character = characters_collection.find_one({"id": character_id}, {"_id": 0})
    return character


@characters_bp.route("/", methods=["GET"])
@characters_bp.route("/filter", methods=["GET"])
def get_characters():
    """
    Fetches the Characters with filtering and sorting when applied
    return : paginated and sorted characters
    """
    characters = list(characters_collection.find({}, {"_id": 0}))  # Alle Charaktere holen

    filtered_characters = filtering(characters) # Filtering'

    sorted_characters = sorting(filtered_characters) # Sorting

    # Pagination
    limit = request.args.get("limit", default=20, type=int)
    skip = request.args.get("skip", default=0, type=int)

    if "limit" not in request.args and "skip" not in request.args and "sort_by" not in request.args:
        random_choice = sample(sorted_characters, min(limit, len(sorted_characters)))
        return jsonify({"characters": random_choice})

    paginated_characters = sorted_characters[skip : skip + limit]
    return jsonify({
        "message": "Characters fetched successfully!",
        "characters": paginated_characters
    }), 200


@characters_bp.route("/<int:id>", methods=["GET"])
def display_character_by_id(id):
    """
    Fetches character data by id
    return : Characterdata belonging to id
    """
    character = get_character_by_id(id)
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
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Auto Increment ID logic by finding last DB-character + 1
    last_character = characters_collection.find_one(sort=[("id", -1)])
    new_id = 1 if last_character is None else last_character["id"] + 1

    new_character = {
        "id": new_id,
        "name": data["name"],
        "house": data.get("house"),
        "animal": data.get("animal"),
        "symbol": data.get("symbol"),
        "nickname": data.get("nickname"),
        "role": data.get("role"),
        "age": data.get("age"),
        "death": data.get("death"),
        "strength": data.get("strength"),
    }

    # Insert into MongoDB
    inserted_character = characters_collection.insert_one(new_character)

    # Fetch inserted character and remove `_id`
    created_character = characters_collection.find_one({"_id": inserted_character.inserted_id}, {"_id": 0})

    return jsonify({
        "message": "Character added successfully!",
        "created_character": created_character
    }), 201


@characters_bp.route("/<int:id>", methods=["PATCH"])
def edit_character(id):
    """
    Updates a (part of a) character by id
    return : Updated Character
    """
    character = get_character_by_id(id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    characters_collection.update_one({"id": id}, {"$set": data})

    updated_character = get_character_by_id(id)

    return jsonify({
        "message": "Character updated successfully!",
        "updated_character": updated_character
    })


@characters_bp.route("/<int:id>", methods=["DELETE"])
def delete_character(id):
    """
    Deletes a character by id from the mongo DB
    return : Delete successfully message
    """
    character = get_character_by_id(id)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    characters_collection.delete_one({"id": id})

    return jsonify({"message": "Character deleted successfully!"})
