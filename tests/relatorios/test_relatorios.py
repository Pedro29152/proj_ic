
def test_relatorios_projetos_2XX(client, admin_token):
    response = client.get(
        '/api/relatorios/projetos',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_relatorios_cursos_2XX(client, admin_token):
    response = client.get(
        '/api/relatorios/cursos',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_relatorios_orientadores_2XX(client, admin_token):
    response = client.get(
        '/api/relatorios/orientadores',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_relatorios_orientador_2XX(client, orientador_token):
    response = client.get(
        '/api/relatorios/orientador',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(orientador_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_relatorios_autores_2XX(client, admin_token):
    response = client.get(
        '/api/relatorios/autores',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

