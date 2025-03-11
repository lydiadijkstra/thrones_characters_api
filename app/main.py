from flask import Flask, jsonify, request

from app.endpoints.characters import characters_bp
from app.endpoints.home import home_bp


def create_app():
    """
    Initialize the storage and the app.
    Run the app.
    """
    print("Welcome at my Game of Thrones Character API")

    app = Flask(__name__)

    app.register_blueprint(home_bp)
    app.register_blueprint(characters_bp)

    return app


app = create_app() # Create the app instance


@app.errorhandler(404)
def not_found(error):
    """
    Function for handling errors for ID out of range in any case
    :param error: error
    :return: error message
    """
    return jsonify({"error": "Character not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001) # Run the server
