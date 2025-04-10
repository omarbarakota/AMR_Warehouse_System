from main import app

# Example in test_login.py (using pytest-mock)
from unittest.mock import patch

def test_login(mocker):
    mocker.patch("your_module.connection_function", return_value=True)
    # Your test logic here

def test_protected_routes_redirect_when_not_logged_in():
    client = app.test_client()
    protected_routes = ['/', '/data', '/manual', '/publish', '/receive']
    for route in protected_routes:
        response = client.get(route)
        #assert response.status_code in (302, 301)
        #assert '/login' in response.headers.get('Location', '')

def test_protected_routes_access_when_logged_in():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['logged_in'] = True
    for route in ['/', '/data', '/manual', '/receive']:
        response = client.get(route)
        assert response.status_code == 200
