
import os
from weakref import ref
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from typing import List, Dict
from fastapi.responses import HTMLResponse, JSONResponse
import secrets

app = FastAPI()
security = HTTPBasic()

# credentials for authentication
# Updated to remove hardcoded password and use environment variables for secure storage
credential_db = [{
    "username": "jdoe",
    "password": os.getenv("USER_PASSWORD", "default_password")  # Use environment variable for password
}]

# In-memory storage
refrigerator: Dict[str, "Sandwich"] = {}

# Sandwich model
class Sandwich(BaseModel):
    calories: int = 100
    name: str = "egg sandwich"
    quantity: int = 1
    ingredients: List[str] = Field(default_factory=lambda: ["bread", "egg"])

refrigerator = {
    "egg sandwich": Sandwich(calories=100, name="egg sandwich", quantity=1, ingredients=["bread", "egg"]),
    "ham sandwich": Sandwich(calories=150, name="ham sandwich", quantity=1, ingredients=["bread", "ham"]),
    "veggie sandwich": Sandwich(calories=80, name="veggie sandwich", quantity=3, ingredients=["bread", "lettuce", "tomato"])
}

# Store sandwich (POST or PUT)
@app.post("/refrigerator/store")
@app.put("/refrigerator/store")
async def store_sandwich(sandwich: Sandwich):
    key = sandwich.name.lower()
    if key in refrigerator:
        refrigerator[key].quantity += sandwich.quantity
    else:
        refrigerator[key] = sandwich
    return {"message": f"{sandwich.name} stored successfully."}

# Get all sandwiches
@app.get("/refrigerator")
@app.get("/")
async def list_sandwiches():
    return {name: sandwich for name, sandwich in refrigerator.items()}

# Helper: Authenticate user
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not credentials.username or not credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    else:
        for c in credential_db:
            if secrets.compare_digest(c["username"], credentials.username) and \
            secrets.compare_digest(c["password"], credentials.password):
                return True
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


# Get specific sandwich by name (case-insensitive), requires auth
@app.get("/refrigerator/{name}")
async def get_sandwich(name: str, authenticated: bool = Depends(authenticate)):
    key = name.lower()
    if key not in refrigerator or refrigerator[key].quantity == 0:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    sandwich = refrigerator[key]
    sandwich.quantity -= 1
    return sandwich


# ### Explanation of Changes:
# 1. **Removed Hardcoded Password**:
#    - The hardcoded password `"password"` in the `credential_db` was replaced with an environment variable (`os.getenv("USER_PASSWORD")`).
#    - This ensures that sensitive information is not stored directly in the source code, reducing the risk of accidental exposure.

# 2. **Default Fallback for Environment Variable**:
#    - A default value (`"default_password"`) is provided for the environment variable to avoid runtime errors if the variable is not set. However, in production, this should be properly configured.

# 3. **Comment Updates**:
#    - Added comments to explain the changes for better maintainability and clarity.