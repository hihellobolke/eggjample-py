import pytest
from fastapi.testclient import TestClient
from main import app, refrigerator, Sandwich # Import app and in-memory store

client = TestClient(app)

# Helper to reset the refrigerator state for each test
@pytest.fixture(autouse=True)
def reset_refrigerator():
    refrigerator.clear()
    refrigerator.update({
        "egg sandwich": Sandwich(calories=100, name="egg sandwich", quantity=1, ingredients=["bread", "egg"]),
        "ham sandwich": Sandwich(calories=150, name="ham sandwich", quantity=1, ingredients=["bread", "ham"]),
        "veggie sandwich": Sandwich(calories=80, name="veggie sandwich", quantity=3, ingredients=["bread", "lettuce", "tomato"])
    })

# --- Test data ---
VALID_USERNAME = "jdoe"
VALID_PASSWORD = "password" # In a real scenario, this should also come from env or config for tests

# --- Tests for /refrigerator/store (POST and PUT) ---

def test_store_new_sandwich_post():
    sandwich_data = {"name": "cheese sandwich", "calories": 120, "quantity": 2, "ingredients": ["bread", "cheese"]}
    response = client.post("/refrigerator/store", json=sandwich_data)
    assert response.status_code == 200
    assert response.json() == {"message": "cheese sandwich stored successfully."}
    assert "cheese sandwich" in refrigerator
    assert refrigerator["cheese sandwich"].quantity == 2

def test_store_existing_sandwich_post():
    sandwich_data = {"name": "egg sandwich", "calories": 100, "quantity": 3, "ingredients": ["bread", "egg"]}
    initial_quantity = refrigerator["egg sandwich"].quantity
    response = client.post("/refrigerator/store", json=sandwich_data)
    assert response.status_code == 200
    assert response.json() == {"message": "egg sandwich stored successfully."}
    assert refrigerator["egg sandwich"].quantity == initial_quantity + 3

def test_store_new_sandwich_put():
    sandwich_data = {"name": "tuna sandwich", "calories": 130, "quantity": 1, "ingredients": ["bread", "tuna"]}
    response = client.put("/refrigerator/store", json=sandwich_data)
    assert response.status_code == 200
    assert response.json() == {"message": "tuna sandwich stored successfully."}
    assert "tuna sandwich" in refrigerator
    assert refrigerator["tuna sandwich"].quantity == 1

def test_store_existing_sandwich_put():
    sandwich_data = {"name": "ham sandwich", "calories": 150, "quantity": 2, "ingredients": ["bread", "ham"]}
    initial_quantity = refrigerator["ham sandwich"].quantity
    response = client.put("/refrigerator/store", json=sandwich_data)
    assert response.status_code == 200
    assert response.json() == {"message": "ham sandwich stored successfully."}
    assert refrigerator["ham sandwich"].quantity == initial_quantity + 2

# --- Tests for /refrigerator and / (GET) ---

def test_list_sandwiches_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "egg sandwich" in data
    assert "ham sandwich" in data
    assert "veggie sandwich" in data
    assert data["egg sandwich"]["quantity"] == 1

def test_list_sandwiches_refrigerator():
    response = client.get("/refrigerator")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3 # Based on initial setup
    assert data["veggie sandwich"]["quantity"] == 3

# --- Tests for /refrigerator/{name} (GET) ---

def test_get_sandwich_success():
    response = client.get("/refrigerator/egg sandwich", auth=(VALID_USERNAME, VALID_PASSWORD))
    assert response.status_code == 200
    sandwich = response.json()
    assert sandwich["name"] == "egg sandwich"
    assert sandwich["quantity"] == 0 # Quantity is decremented after retrieval
    assert refrigerator["egg sandwich"].quantity == 0 # Verify in-memory store

def test_get_sandwich_case_insensitive():
    response = client.get("/refrigerator/EGG SANDWICH", auth=(VALID_USERNAME, VALID_PASSWORD))
    assert response.status_code == 200
    sandwich = response.json()
    assert sandwich["name"] == "egg sandwich"
    assert refrigerator["egg sandwich"].quantity == 0

def test_get_sandwich_not_found():
    response = client.get("/refrigerator/nonexistent sandwich", auth=(VALID_USERNAME, VALID_PASSWORD))
    assert response.status_code == 404
    assert response.json() == {"detail": "Sandwich not found"}

def test_get_sandwich_quantity_zero():
    # First, get the sandwich to make its quantity zero
    client.get("/refrigerator/egg sandwich", auth=(VALID_USERNAME, VALID_PASSWORD))
    # Try to get it again
    response = client.get("/refrigerator/egg sandwich", auth=(VALID_USERNAME, VALID_PASSWORD))
    assert response.status_code == 404
    assert response.json() == {"detail": "Sandwich not found"} # Because quantity is 0

def test_get_sandwich_unauthorized_no_creds():
    response = client.get("/refrigerator/egg sandwich")
    assert response.status_code == 401 # FastAPI TestClient handles basic auth prompt
    # Depending on exact TestClient behavior with missing auth,
    # you might get a response that indicates WWW-Authenticate header.
    # For simplicity, we check status. The detail might vary.
    assert "Unauthorized" in response.json().get("detail", "") or response.headers.get("www-authenticate") == "Basic"


def test_get_sandwich_unauthorized_wrong_creds():
    response = client.get("/refrigerator/egg sandwich", auth=(VALID_USERNAME, "wrongpassword"))
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

def test_get_sandwich_unauthorized_wrong_username():
    response = client.get("/refrigerator/egg sandwich", auth=("wronguser", VALID_PASSWORD))
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}