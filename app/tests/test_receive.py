from main import app

def test_receive_message():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['logged_in'] = True
    response = client.get('/receive')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "Receiving via MQTT. Check logs for messages."
