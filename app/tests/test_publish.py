import json
from main import app

# Example in test_login.py (using pytest-mock)
from unittest.mock import patch

def test_login(mocker):
    mocker.patch("your_module.connection_function", return_value=True)
    # Your test logic here

def test_publish_message():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['logged_in'] = True
    payload = {'topic': 'test/topic', 'message': 'hello world'}
    response = client.post('/publish', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "Message published"
    assert data['topic'] == "test/topic"
    assert data['message'] == "hello world"
