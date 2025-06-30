from app.main import app

def test_logout_clears_session():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['logged_in'] = True
    response = client.get('/logout', follow_redirects=True)
    assert b"login" in response.data
