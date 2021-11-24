
def test_get_anos_response_2XX(client):
    response = client.get('/api/dashboard/anos')

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_ano_response_2XX(client):
    response = client.get('/api/dashboard/projetospeloano')

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_semestre_response_2XX(client):
    response = client.get('/api/dashboard/projetospelosemestre')

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_curso_2XX(client):
    response = client.get('/api/dashboard/projetosporcurso')

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_orientador_2XX(client, admin_token):
    response = client.get(
        '/api/dashboard/projetospororientador',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_orientador_self_2XX(client, orientador_token):
    response = client.get(
        '/api/dashboard/projetospororientadorself',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(orientador_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_formandos_curso_2XX(client, admin_token):
    response = client.get(
        '/api/dashboard/formandosporcurso',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_status_2XX(client, admin_token):
    response = client.get(
        '/api/dashboard/projetosporstatus',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_modalidade_2XX(client):
    response = client.get('/api/dashboard/projetospormodalidade')

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_projetos_solicitacoes_2XX(client, admin_token):
    response = client.get(
        '/api/dashboard/solicitacoes',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_dashboard_usuarios_2XX(client, admin_token):
    response = client.get(
        '/api/dashboard/usuarios',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300
