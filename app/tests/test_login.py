import pytest
from main import app

# Example in test_login.py (using pytest-mock)
from unittest.mock import patch

def test_login(mocker):
    mocker.patch("your_module.connection_function", return_value=True)
    # Your test logic here

def test_login_success():
    client = app.test_client()
    response = client.post('/login', data={'username': 'admin', 'password': '123'}, follow_redirects=True)
    assert response.status_code == 200
    #assert b"dashboard" in response.data or b"index" in response.data

def test_login_failure():
    client = app.test_client()
    response = client.post('/login', data={'username': 'admin', 'password': 'wrongpass'})
    assert b"Invalid username or password" in response.data
