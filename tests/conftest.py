from os.path import dirname, isfile, join
import json

import pytest
from dotenv import load_dotenv

# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '../.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


@pytest.fixture(scope='session')
def client():
    from biblioteca import create_app
    # instancia nossa função factory criada anteriormente
    flask_app = create_app('testing')

    # O Flask fornece um caminho para testar a aplicação
    # utilizando o Werkzeug test Client
    # e manipulando o contexto (configurações)
    testing_client = flask_app.test_client()

    # Antes de executar os testes, é criado um contexto com as configurações
    # da aplicação
    ctx = flask_app.app_context()
    ctx.push()

    reponse = testing_client.post('/api/auth/login', data={'username': 'admin', 'password':'123'})
    admin_token = json.loads(reponse.data.decode('UTF-8'))['token']

    
    # retorna o client criado
    yield {
        'client': testing_client,
        'admin_token':admin_token
    }  # this is where the testing happens!

    # remove o contexto ao terminar os testes
    ctx.pop()
