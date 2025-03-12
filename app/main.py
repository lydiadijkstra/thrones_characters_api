from flask import Flask, jsonify
from pymongo import MongoClient

# MongoDB Verbindung initialisieren
client = MongoClient("mongodb://localhost:27017/")
db = client["thrones_db"]
characters_collection = db["characters"]

def create_app():
    """
    Initialize the storage and the app.
    Run the app.
    """
    print("Welcome to my Game of Thrones Character API")

    app = Flask(__name__)

    # Importiere Blueprints erst nach der App-Initialisierung
    from app.endpoints.characters import create_characters_blueprint
    from app.endpoints.home import home_bp

    # Blueprint registrieren (characters_bp erst hier erzeugen!)
    characters_bp = create_characters_blueprint(characters_collection)

    app.register_blueprint(home_bp)
    app.register_blueprint(characters_bp)

    return app

app = create_app()  # Erstelle die App-Instanz

@app.errorhandler(404)
def not_found(error):
    """
    Function for handling errors for ID out of range in any case
    :param error: error
    :return: error message
    """
    return jsonify({"error": "Character not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Server starten
