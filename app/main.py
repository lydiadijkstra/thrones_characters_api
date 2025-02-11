from flask import Flask, jsonify, request

from app.core.database import initialize_database
from app.endpoints.characters import characters_bp
from app.endpoints.home import home_bp

app = Flask(__name__)


def create_app():
    """
    Initialize the storage and the app.
    Run the app.
    """
    print("Welcome at my Game of Thrones Character API")

    #app = Flask(__name__)
    initialize_database()
    app.register_blueprint(home_bp)
    app.register_blueprint(characters_bp)

    return app


if __name__ == "__main__":
    create_app() # Create the app instance
    app.run(debug=True) # Run the server
