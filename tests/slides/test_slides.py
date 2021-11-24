import io, json

def test_slides_POST_2XX(client, admin_token):
    data = {
        'titulo': '',
        'subTitulo': '',
        'title': '', 
        'subTitle': ''
    }
    data['file'] = (io.BytesIO(b"abcdef"), 'teste.jpg')
    
    response1 = client.post(
        '/api/slides',
        data=data,
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    data['file'] = (io.BytesIO(b"abcdef"), 'teste1.jpg')
    response2 = client.post(
        '/api/slides',
        data=data,
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert (response1.status_code >= 200 and response1.status_code < 300) and (response2.status_code >= 200 and response2.status_code < 300)

def test_slides_GET_2XX(client):
    response = client.get('/api/slides')

    assert response.status_code >= 200 and response.status_code < 300

def test_get_slide_2XX(client):
    slides = client.get('/api/slides')
    slides_obj = json.loads(slides.data.decode('UTF-8'))[0]
    if not slides_obj:
        raise Exception('Nenhum slide cadastrado')

    response = client.get('/api/slides/{0}'.format(slides_obj['codSlide']))

    assert response.status_code >= 200 and response.status_code < 300

def test_edit_slide_2XX(client, admin_token):
    slides = client.get('/api/slides')
    slides_obj = json.loads(slides.data.decode('UTF-8'))[0]
    if not slides_obj:
        raise Exception('Nenhum slide cadastrado')

    response = client.put(
        '/api/slides/{0}'.format(slides_obj['codSlide']),
        data={
            'titulo': '',
            'subTitulo': '',
            'title': '',
            'subTitle': ''
        },
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_remove_slide_2XX(client, admin_token):
    slides = client.get('/api/slides')
    slides_obj = json.loads(slides.data.decode('UTF-8'))[0]
    if not slides_obj:
        raise Exception('Nenhum slide cadastrado')

    response = client.delete(
        '/api/slides/{0}'.format(slides_obj['codSlide']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300
