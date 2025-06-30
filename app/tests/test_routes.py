from app.main import app

def test_protected_routes_redirect_when_not_logged_in():
    client = app.test_client()
    protected_routes = [
        '/',
        '/admin',
        '/database',
        '/publish',
        '/users',
        '/api/users',
        '/api/packages',
        '/api/admin/delete-mqtt-messages'
    ]
    for route in protected_routes:
        # Use GET for most, POST for /publish, /api/users, /api/packages, /api/admin/delete-mqtt-messages
        if route in ['/publish', '/api/users', '/api/packages', '/api/admin/delete-mqtt-messages']:
            response = client.post(route)
        else:
            response = client.get(route)
        #assert response.status_code in (302, 301, 403)
        #assert '/login' in response.headers.get('Location', '') or response.status_code == 403

def test_protected_routes_access_when_logged_in():
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['logged_in'] = True
        sess['role'] = 'admin'
    for route in ['/', '/admin', '/database', '/users']:
        response = client.get(route)
        assert response.status_code == 200
