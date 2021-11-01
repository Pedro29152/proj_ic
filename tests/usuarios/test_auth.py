
USUARIO_ADMIN = 'admin'
SENHA_ADMIN = '123'

def test_login_admin_200(client):
    response = client.post(
        '/api/auth/login', 
        data={'username': USUARIO_ADMIN, 'password': SENHA_ADMIN}
    )

    assert response.status_code >= 200 and response.status_code < 300
