import pytest, random

from os.path import dirname, isfile, join
from dotenv import load_dotenv

_ENV_FILE = join(dirname(__file__), '..', '.env')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

import json

from biblioteca.db import Db, get_db
from biblioteca import create_app

APP = create_app('testing')
CLIENT = APP.test_client()

@pytest.fixture(scope='session')
def client():
    ctx = APP.app_context()
    ctx.push()
    ctx.g.db = Db(commit_on_exit=False)

    yield CLIENT

    db = ctx.g.pop('db', None)
    db.rollback()
    db.close()
    ctx.pop()

@pytest.fixture(scope='session')
def admin_token(client):
    response = client.post('/api/auth/login', data={'username': 'admin', 'password':'123'})
    admin_token = json.loads(response.data.decode('UTF-8'))['token']

    yield admin_token

@pytest.fixture(scope='session')
def orientador_criado(client, admin_token):
    ra = '91822'
    nome_rng = 'nome_{}'.format(random.randint(0,100000000))
    response = client.post(
        '/api/orientadores',
        data={
            'nomeOrientador': nome_rng,
            'raOrientador': ra,
            'email': 'email@teste.com',
            'linkCurrLattes': 'https://teste.com/teste'
        },
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)}
    )
    if not (response.status_code >= 200 and response.status_code < 300):
        raise ValueError('Erro ao cadastrar orientador')
    
    from biblioteca.orientador import orientadores_dao
    db = get_db()
    oriDao = orientadores_dao.OrientadoresDAO(db)
    orientador = oriDao.get_orientador(ra)
    yield orientador

@pytest.fixture(scope='session')
def usuario_orientador_criado(client, admin_token, orientador_criado):
    response = client.post(
        '/api/usuarios/cadastro/orientador/existente',
        data={
            'nome': orientador_criado.nomeOrientador,
            'email': orientador_criado.email,
            'codOrientador': orientador_criado.codOrientador
        },
        headers={'AUTHORIZATION': 'Bearer {0}'.format(admin_token)})
    resp = json.loads(response.data.decode('UTF-8'))
    user = {'username': orientador_criado.raOrientador, 'password': resp['password']}
    yield user

@pytest.fixture(scope='session')
def orientador_token(client, usuario_orientador_criado):
    response = client.post('/api/auth/login', data={'username': usuario_orientador_criado['username'], 'password':usuario_orientador_criado['password']})
    orientador_token = json.loads(response.data.decode('UTF-8'))['token']

    yield orientador_token
