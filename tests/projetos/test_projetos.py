import json

def test_busca_projetos_carregados_2XX(client):
    response = client['client'].get('/api/projetos')

    assert response.status_code >= 200 and response.status_code < 300


# def test_cadastro_projeto(client):        
#     response = client.post('/api/projetos/cadastrar', headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidGlwb1VzdWFyaW8iOiI0IiwiZXh0IjoiMjAyMC0wNS0yOSAxNTozODo0MS42Njc2NjMifQ.49IMXbzgU9zpruJbKc7F5QBi8vCr1yszWc2UpoVYY0M'})
#     data = json.loads(response.data.decode("utf-8"))
#     assert response.status_code >= 200 and response.status_code < 300