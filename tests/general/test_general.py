
def test_index_response_2XX(client):
    response = client.get('/')

    assert response.status_code >= 200 and response.status_code < 300

def test_api_index_response_2XX(client):
    response = client.get('/api')

    assert response.status_code >= 200 and response.status_code < 300

def test_allcounts_response_2XX(client, admin_token):
    response = client.get('/api/allcounts', headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)})

    assert response.status_code >= 200 and response.status_code < 300

def test_contato_response_2XX(client):
    response = client.post(
        '/api/contato', 
        data={
            'email':'email.teste@teste.com',
            'nome':'teste',
            'assunto':'TESTE',
            'mensagem':'teste zica kkkkk'
        }
    )
    
    assert response.status_code >= 200 and response.status_code < 300

def test_enum_tipo_usuario_response_2XX(client, admin_token):
    response = client.get('/api/enum/tipousuario', headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)})

    assert response.status_code >= 200 and response.status_code < 300

def test_enum_tipo_orientador_response_2XX(client):
    response = client.get('/api/enum/tipoorientador')

    assert response.status_code >= 200 and response.status_code < 300

def test_enum_status_projeto_response_2XX(client, admin_token):
    response = client.get('/api/enum/statusprojeto', headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)})

    assert response.status_code >= 200 and response.status_code < 300

def test_enum_linguagem_projeto_response_2XX(client):
    response = client.get('/api/enum/linguagemprojeto')

    assert response.status_code >= 200 and response.status_code < 300

def test_enum_modalidade_projeto_response_2XX(client):
    response = client.get('/api/enum/modalidadeprojeto')

    assert response.status_code >= 200 and response.status_code < 300
