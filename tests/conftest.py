from os.path import dirname, isfile, join
import json

from biblioteca.db import Db
from biblioteca import create_app

import pytest
from dotenv import load_dotenv

# instancia nossa função factory criada anteriormente
APP = create_app('testing')
# O Flask fornece um caminho para testar a aplicação
# utilizando o Werkzeug test Client
# e manipulando o contexto (configurações)
CLIENT = APP.test_client()

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '../.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)

@pytest.fixture(scope='session')
def client():

    # Antes de executar os testes, é criado um contexto com as configurações
    # da aplicação
    ctx = APP.app_context()
    ctx.push()

    # retorna o client criado
    yield CLIENT # this is where the testing happens!

    # remove o contexto ao terminar os testes
    ctx.pop()

@pytest.fixture(scope='session')
def admin_token():
    ctx = APP.app_context()
    ctx.push()

    reponse = CLIENT.post('/api/auth/login', data={'username': 'admin', 'password':'123'})
    admin_token = json.loads(reponse.data.decode('UTF-8'))['token']

    yield admin_token
    
    ctx.pop()
