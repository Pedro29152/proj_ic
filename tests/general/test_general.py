
def test_index_response_200(client):
    response = client.get('/')
    
    assert response.status_code == 200

def test_api_index_response_200(client):
    response = client.get('/api')
    
    assert response.status_code == 200
