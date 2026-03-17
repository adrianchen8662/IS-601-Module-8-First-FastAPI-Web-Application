# tests/integration/test_fastapi_calculator.py

import pytest  # Import the pytest framework for writing and running tests
from unittest.mock import patch  # Import patch for mocking internal functions
from fastapi.testclient import TestClient  # Import TestClient for simulating API requests
from main import app, OperationRequest  # Import the FastAPI app and request model

# ---------------------------------------------
# Pytest Fixture: client
# ---------------------------------------------

@pytest.fixture
def client():
    """
    Pytest Fixture to create a TestClient for the FastAPI application.

    This fixture initializes a TestClient instance that can be used to simulate
    requests to the FastAPI application without running a live server. The client
    is yielded to the test functions and properly closed after the tests complete.

    Benefits:
    - Speeds up testing by avoiding the overhead of running a server.
    - Allows for testing API endpoints in isolation.
    """
    with TestClient(app) as client:
        yield client  # Provide the TestClient instance to the test functions

# ---------------------------------------------
# Test Function: test_add_api
# ---------------------------------------------

def test_add_api(client):
    """
    Test the Addition API Endpoint.

    This test verifies that the `/add` endpoint correctly adds two numbers provided
    in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/add` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`15`).
    """
    # Send a POST request to the '/add' endpoint with JSON payload
    response = client.post('/add', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 15, f"Expected result 15, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_subtract_api
# ---------------------------------------------

def test_subtract_api(client):
    """
    Test the Subtraction API Endpoint.

    This test verifies that the `/subtract` endpoint correctly subtracts the second number
    from the first number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/subtract` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/subtract' endpoint with JSON payload
    response = client.post('/subtract', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_multiply_api
# ---------------------------------------------

def test_multiply_api(client):
    """
    Test the Multiplication API Endpoint.

    This test verifies that the `/multiply` endpoint correctly multiplies two numbers
    provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/multiply` endpoint with JSON data `{'a': 10, 'b': 5}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`50`).
    """
    # Send a POST request to the '/multiply' endpoint with JSON payload
    response = client.post('/multiply', json={'a': 10, 'b': 5})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 50, f"Expected result 50, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_api
# ---------------------------------------------

def test_divide_api(client):
    """
    Test the Division API Endpoint.

    This test verifies that the `/divide` endpoint correctly divides the first number
    by the second number provided in the JSON payload and returns the expected result.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 2}`.
    2. Assert that the response status code is `200 OK`.
    3. Assert that the JSON response contains the correct result (`5`).
    """
    # Send a POST request to the '/divide' endpoint with JSON payload
    response = client.post('/divide', json={'a': 10, 'b': 2})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Assert that the JSON response contains the correct 'result' value
    assert response.json()['result'] == 5, f"Expected result 5, got {response.json()['result']}"

# ---------------------------------------------
# Test Function: test_divide_by_zero_api
# ---------------------------------------------

def test_divide_by_zero_api(client):
    """
    Test the Division by Zero API Endpoint.

    This test verifies that the `/divide` endpoint correctly handles division by zero
    by returning an appropriate error message and status code.

    Steps:
    1. Send a POST request to the `/divide` endpoint with JSON data `{'a': 10, 'b': 0}`.
    2. Assert that the response status code is `400 Bad Request`.
    3. Assert that the JSON response contains an 'error' field with the message "Cannot divide by zero!".
    """
    # Send a POST request to the '/divide' endpoint with JSON payload attempting division by zero
    response = client.post('/divide', json={'a': 10, 'b': 0})
    
    # Assert that the response status code is 400 (Bad Request), indicating an error occurred
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    
    # Assert that the JSON response contains an 'error' field
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"
    
    # Assert that the 'error' field contains the correct error message
    assert "Cannot divide by zero!" in response.json()['error'], \
        f"Expected error message 'Cannot divide by zero!', got '{response.json()['error']}'"

def test_get_root(client):
    response = client.get('/')

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "Hello World" in response.text, "Expected 'Hello World' in response body"

def test_invalid_input_missing_field(client):
    response = client.post('/add', json={'a': 10})

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

def test_invalid_input_non_numeric(client):
    response = client.post('/add', json={'a': 'not_a_number', 'b': 5})

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

def test_add_internal_error(client):
    with patch('main.add', side_effect=RuntimeError("unexpected error")):
        response = client.post('/add', json={'a': 10, 'b': 5})

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

def test_subtract_internal_error(client):
    with patch('main.subtract', side_effect=RuntimeError("unexpected error")):
        response = client.post('/subtract', json={'a': 10, 'b': 5})

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

def test_multiply_internal_error(client):
    with patch('main.multiply', side_effect=RuntimeError("unexpected error")):
        response = client.post('/multiply', json={'a': 10, 'b': 5})

    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    assert 'error' in response.json(), "Response JSON does not contain 'error' field"

def test_divide_internal_error(client):
    with patch('main.divide', side_effect=RuntimeError("unexpected error")):
        response = client.post('/divide', json={'a': 10, 'b': 2})

    assert response.status_code == 500, f"Expected status code 500, got {response.status_code}"

def test_validate_numbers_raises_for_non_numeric():
    with pytest.raises(ValueError, match="Both a and b must be numbers."):
        OperationRequest.validate_numbers("not_a_number")