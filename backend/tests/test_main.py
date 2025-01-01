from fastapi.testclient import TestClient # TestClient is a class that will be used to test the API
from main import app # This is the FastAPI instance that we created in main.py

# This is the TestClient instance that we will use to test the API. It will be used to make requests to the API.
client = TestClient(app)

def test_index():
    """Test the index route."""
    response = client.get("/") # Make a GET request to the index route
    assert response.status_code == 200 # Check if the response status code is 200
    assert response.json() == {"message": "Hello World"} # Check if the response JSON is as expected