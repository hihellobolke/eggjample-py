# FastAPI Refrigerator Management System

## Project Description
This project is a simple **Refrigerator Management System** built using FastAPI. It allows users to store, retrieve, and manage sandwiches in an in-memory refrigerator. The system supports basic authentication for retrieving specific sandwiches and provides endpoints for listing, adding, and updating sandwiches.

The project is designed to demonstrate the use of FastAPI for building RESTful APIs, including features like request validation, dependency injection, and authentication.

---

## Project Structure

### 1. `main.py`
This is the core application file that defines the FastAPI app and its endpoints.

- **`Sandwich` Model**: A Pydantic model representing a sandwich with attributes like `calories`, `name`, `quantity`, and `ingredients`.
- **In-Memory Storage**: The `refrigerator` dictionary acts as a simple in-memory database to store sandwich data.
- **Endpoints**:
  - `POST /refrigerator/store` and `PUT /refrigerator/store`: Add or update sandwiches in the refrigerator.
  - `GET /refrigerator` and `GET /`: List all sandwiches in the refrigerator.
  - `GET /refrigerator/{name}`: Retrieve a specific sandwich by name (requires authentication).
- **Authentication**: Basic authentication is implemented using FastAPI's `HTTPBasic` dependency.

### 2. `test_main.py`
This file contains unit tests for the application using `pytest` and FastAPI's `TestClient`.

- **Fixtures**:
  - `reset_refrigerator`: Resets the in-memory refrigerator state before each test.
- **Test Cases**:
  - Tests for storing sandwiches (`POST` and `PUT`).
  - Tests for listing sandwiches (`GET`).
  - Tests for retrieving sandwiches by name, including authentication and error handling.

---

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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

---

## Usage Examples

### 1. Store a New Sandwich
- **Endpoint**: `POST /refrigerator/store`
- **Request Body**:
  ```json
  {
    "name": "cheese sandwich",
    "calories": 120,
    "quantity": 2,
    "ingredients": ["bread", "cheese"]
  }
  ```
- **Response**:
  ```json
  {
    "message": "cheese sandwich stored successfully."
  }
  ```

### 2. List All Sandwiches
- **Endpoint**: `GET /refrigerator`
- **Response**:
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

### 3. Retrieve a Sandwich by Name
- **Endpoint**: `GET /refrigerator/egg sandwich`
- **Authentication**: Basic Auth (`username: jdoe`, `password: password`)
- **Response**:
  ```json
  {
    "calories": 100,
    "name": "egg sandwich",
    "quantity": 0,
    "ingredients": ["bread", "egg"]
  }
  ```

---

## Testing Instructions

1. Install `pytest`:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   pytest test_main.py
   ```

3. Test Coverage:
   - The tests cover all major functionalities, including storing sandwiches, listing sandwiches, retrieving sandwiches, and authentication.

---

## Notes
- This project uses an in-memory database (`refrigerator` dictionary), so data will reset every time the application restarts.
- Authentication is implemented using basic credentials stored in memory. For production, consider using a secure database and environment variables for credentials.

```
