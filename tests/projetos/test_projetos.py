import json

def test_busca_projetos_2XX(client):
    response = client.get('/api/projetos')

    assert response.status_code >= 200 and response.status_code < 300
