# Sandwich Refrigerator API

## Project Description

The Sandwich Refrigerator API is a FastAPI-based application designed to manage an in-memory refrigerator of sandwiches. It allows users to store, retrieve, and list sandwiches with features like authentication for secure access to specific endpoints. This project is ideal for demonstrating RESTful API design, authentication mechanisms, and in-memory data management.

## Project Structure

The project consists of the following components:

### `main.py`
- **Purpose**: Implements the core API functionality.
- **Key Features**:
  - **Endpoints**:
    - `POST /refrigerator/store` and `PUT /refrigerator/store`: Store new sandwiches or update the quantity of existing ones.
    - `GET /refrigerator` and `GET /`: List all sandwiches in the refrigerator.
    - `GET /refrigerator/{name}`: Retrieve a specific sandwich by name (case-insensitive) with authentication.
  - **Authentication**: Basic authentication using username and password.
  - **In-Memory Storage**: Stores sandwich data in a dictionary for quick access and manipulation.
  - **Models**: Defines a `Sandwich` model using Pydantic for data validation.

### `test_main.py`
- **Purpose**: Contains unit tests for the API to ensure its functionality and reliability.
- **Key Features**:
  - Tests for storing sandwiches (`POST` and `PUT`).
  - Tests for listing sandwiches (`GET`).
  - Tests for retrieving sandwiches by name, including authentication and edge cases (e.g., unauthorized access, non-existent sandwiches, zero quantity).

### `hello.py`
- **Purpose**: A simple script that prints "Hello, World!".
- **Key Features**: Serves as a placeholder or example script unrelated to the main API functionality.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Usage Examples

1. **Store a new sandwich**:
   - Endpoint: `POST /refrigerator/store`
   - Request Body:
     ```json
     {
       "name": "cheese sandwich",
       "calories": 120,
       "quantity": 2,
       "ingredients": ["bread", "cheese"]
     }
     ```
   - Response:
     ```json
     {
       "message": "cheese sandwich stored successfully."
     }
     ```

2. **List all sandwiches**:
   - Endpoint: `GET /refrigerator`
   - Response:
     ```json
     {
       "egg sandwich": {
         "calories": 100,
         "name": "egg sandwich",
         "quantity": 1,
         "ingredients": ["bread", "egg"]
       },
       "ham sandwich": {
         "calories": 150,
         "name": "ham sandwich",
         "quantity": 1,
         "ingredients": ["bread", "ham"]
       }
     }
     ```

3. **Retrieve a sandwich by name**:
   - Endpoint: `GET /refrigerator/egg sandwich`
   - Authentication: Basic Auth (username: `jdoe`, password: `password`)
   - Response:
     ```json
     {
       "calories": 100,
       "name": "egg sandwich",
       "quantity": 0,
       "ingredients": ["bread", "egg"]
     }
     ```

## Testing Instructions

1. Install `pytest`:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   pytest test_main.py
   ```

3. **Test Coverage**:
   - Tests cover storing sandwiches, listing sandwiches, retrieving sandwiches, and authentication scenarios.
   - Ensure the refrigerator state resets between tests using the `reset_refrigerator` fixture.

## Notes

- Authentication credentials are hardcoded for simplicity (`jdoe`/`password`). In a production environment, use secure methods to manage credentials.
- The in-memory storage is reset each time the application restarts. For persistent storage, integrate a database.
          "ingredients": ["bread","egg"]
        }
        ```

## Testing Instructions

The project uses `pytest` for running unit tests. The tests are located in `test_main.py`.

1.  **Ensure `pytest` and `httpx` are installed** (they are included in the `pip install` command in the Installation section if you installed all suggested development dependencies).

2.  **Run tests:**
    Navigate to the root directory of the project in your terminal and run:
    ```bash
    pytest
    ```
    Pytest will automatically discover and run the tests in `test_main.py`. You should see output indicating the number of tests passed.

This README provides a comprehensive overview of the Eggjample FastAPI Sandwich API, including its setup, usage, and testing procedures.
