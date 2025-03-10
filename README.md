Here’s a basic README template for your API. You can customize it further based on your needs:


# Game of Thrones Character API

This API provides access to a database of Game of Thrones characters, allowing users to interact with character data using various CRUD operations. It supports retrieving, adding, editing, and deleting characters, as well as querying characters with pagination and filtering.

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [GET /characters](#get-characters)
  - [GET /characters/{id}](#get-character-by-id)
  - [POST /characters](#add-character)
  - [PATCH /characters/{id}](#edit-character)
  - [DELETE /characters/{id}](#delete-character)
- [Running Tests](#running-tests)
- [License](#license)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/game-of-thrones-api.git
   ```

2. Navigate to the project directory:
   ```bash
   cd game-of-thrones-api
   ```

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database (if not already set up):
   ```bash
   # Run the migrations or set up the database here (example command)
   python manage.py db upgrade
   ```

6. Run the application:
   ```bash
   export FLASK_APP=app.main
    flask run
   ```

   The API will now be accessible at `http://localhost:5000`.

## API Endpoints

### `GET /characters`

Fetch a list of characters with optional pagination.

- **Query Parameters**:
  - `limit`: The maximum number of characters to return (default: 20).
  - `skip`: The number of characters to skip (default: 0).

#### Example Request:
```bash
GET /characters?limit=10&skip=5
```

#### Example Response:
```json
[
  {
    "id": 1,
    "name": "Jon Snow",
    "house": "Stark",
    "animal": "Direwolf",
    "symbol": "Wolf",
    "nickname": "King in the North",
    "role": "King",
    "age": 25,
    "death": null,
    "strength": "Physically strong"
  },
  ...
]
```

### `GET /characters/{id}`

Fetch a character by ID.

#### Example Request:
```bash
GET /characters/1
```

#### Example Response:
```json
{
  "id": 1,
  "name": "Jon Snow",
  "house": "Stark",
  "animal": "Direwolf",
  "symbol": "Wolf",
  "nickname": "King in the North",
  "role": "King",
  "age": 25,
  "death": null,
  "strength": "Physically strong"
}
```

### `POST /characters`

Add a new character to the database.

#### Example Request:
```bash
POST /characters
{
  "name": "Mock Data",
  "house": "Mock House",
  "animal": "Mock Animal",
  "symbol": "Mock Symbol",
  "nickname": "Mock Nickname",
  "role": "Mock role",
  "age": 25,
  "death": null,
  "strength": "Mock Strength"
}
```

#### Example Response:
```json
{
  "created_character": {
    "id": 51,
    "name": "Mock Data",
    "house": "Mock House",
    "animal": "Mock Animal",
    "symbol": "Mock Symbol",
    "nickname": "Mock Nickname",
    "role": "Mock role",
    "age": 25,
    "death": null,
    "strength": "Mock Strength"
  },
  "message": "Character added successfully!"
}
```

### `PATCH /characters/{id}`

Update an existing character's details.

#### Example Request:
```bash
PATCH /characters/1
{
  "name": "Updated Data",
  "house": "Updated House",
  "animal": "Updated Animal",
  "symbol": "Updated Symbol",
  "nickname": "Updated Nickname",
  "role": "Updated role",
  "age": 30,
  "death": null,
  "strength": "Updated Strength"
}
```

#### Example Response:
```json
{
  "message": "Character updated successfully!",
  "updated_character": {
    "id": 1,
    "name": "Updated Data",
    "house": "Updated House",
    "animal": "Updated Animal",
    "symbol": "Updated Symbol",
    "nickname": "Updated Nickname",
    "role": "Updated role",
    "age": 30,
    "death": null,
    "strength": "Updated Strength"
  }
}
```

### `DELETE /characters/{id}`

Delete a character by ID.

#### Example Request:
```bash
DELETE /characters/1
```

#### Example Response:
```json
{
  "message": "Character deleted successfully!"
}
```

## Running Tests

1. Install the testing dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the tests:
   ```bash
   pytest
   ```

   The tests will check the functionality of all endpoints and ensure the API behaves as expected. 


3. Run pytest-cov:
   ```bash
   pytest --cov=app --cov-report=term-missing
   ```

   The test-coverage will check the tests-coverage of the app-files

Terminal outcome example:

---------- coverage: platform darwin, python 3.12.3-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/__init__.py                     0      0   100%
app/core/__init__.py                0      0   100%
app/core/database.py               18     18     0%   2-36
-------------------------------------------------------------
TOTAL                              18     18    66%

The file app/core/database does not run when the test-file runs.
Underneath missing, all the not tested lines in that file are named.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
