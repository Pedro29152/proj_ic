from biblioteca.extensions import TiposUsuario
import json, random

def test_cadastro_usuario_secretaria_2XX(client, admin_token):
    rng = random.randint(0,100000000)
    response = client.post(
        '/api/usuarios/cadastro',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)},
        data={
            'username':'SECRETARIA{0}'.format(rng),
            'password':'123',
            'tipoUsuario': TiposUsuario.Secretaria.value,
            'nome':'secretaria_TEST',
            'email':'secretaria{0}@teste.test'.format(rng)
        }
    )

    r = json.loads(response.data.decode('UTF-8'))

    assert response.status_code >= 200 and response.status_code < 300

def test_busca_usuarios_2XX(client, admin_token):
    response = client.get(
        '/api/usuarios/buscar',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_busca_usuarios_inativos_2XX(client, admin_token):
    response = client.get(
        '/api/usuarios/buscar/inativos',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_editar_usuario_2XX(client, admin_token):
    rng = random.randint(0,100000000)
    usuarios = client.get(
        '/api/usuarios/buscar?nomeUsuario=SECRETARIA',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    usuario_obj = json.loads(usuarios.data.decode('UTF-8'))['data'][0]

    response = client.put(
        '/api/usuarios/{0}'.format(usuario_obj['codUsuario']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)},
        data={
            'nome': 'secretaria_TEST',
            'email': 'secretaria{0}@teste.test'.format(rng),
            'nomeUsuario': 'SECRETARIA{0}'.format(rng),
            'tipoUsuario': TiposUsuario.Secretaria.value
        }
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_editar_senha_usuario_2XX(client, admin_token):
    rng = random.randint(0,100000000)
    usuarios = client.get(
        '/api/usuarios/buscar?nomeUsuario=SECRETARIA',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    usuario_obj = json.loads(usuarios.data.decode('UTF-8'))['data'][0]

    response = client.put(
        '/api/usuarios/mudarsenha/{0}'.format(usuario_obj['codUsuario']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)},
        data={
            'senha': '123'
        }
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_editar_proprio_usuario_2XX(client, admin_token):
    response = client.put(
        '/api/usuarios/edit',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)},
        data={
            'nome':'adminkkk',
            'email':'adminkkk@admin.com'
        }
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_desativa_usuario_2XX(client, admin_token):
    usuarios = client.get(
        '/api/usuarios/buscar?nomeUsuario=SECRETARIA',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    usuario_obj = json.loads(usuarios.data.decode('UTF-8'))['data'][0]

    response = client.delete(
        '/api/usuarios/desativar/{0}'.format(usuario_obj['codUsuario']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_ativa_usuario_2XX(client, admin_token):
    usuarios = client.get(
        '/api/usuarios/buscar/inativos?nomeUsuario=SECRETARIA',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    usuario_obj = json.loads(usuarios.data.decode('UTF-8'))['data'][0]

    response = client.post(
        '/api/usuarios/ativar/{0}'.format(usuario_obj['codUsuario']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

def test_deletar_usuario_2XX(client, admin_token):
    usuarios = client.get(
        '/api/usuarios/buscar?nomeUsuario=SECRETARIA',
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    usuario_obj = json.loads(usuarios.data.decode('UTF-8'))['data'][0]

    response = client.delete(
        '/api/usuarios/{0}'.format(usuario_obj['codUsuario']),
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )

    assert response.status_code >= 200 and response.status_code < 300

