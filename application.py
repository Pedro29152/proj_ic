# -*- coding: utf-8 -*-

import sys

from os import getenv
from os.path import dirname, isfile, join, abspath


from dotenv import load_dotenv


# a partir do arquivo atual adicione ao path o arquivo .env
_ENV_FILE = join(dirname(__file__), '.env')

# existindo o arquivo faça a leitura do arquivo através da função load_dotenv
if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


from biblioteca import create_app

# instancia nossa função factory criada anteriormente
app = create_app(getenv('FLASK_ENV') or 'default')

def run():
    conf = {
        'ip': '0.0.0.0',
        'port': app.config['APP_PORT'],
        'debug': app.config['DEBUG']
    }

    if len(sys.argv) > 1:
        comandos = {}

        for i, arg in enumerate(sys.argv):
            if i == 0:
                continue
            
            if arg[:2] == '--':
                param = arg[2:].split('=')
                comandos[param[0]] = param[1]

        conf = {**conf, **comandos}

    # executa o servidor web do flask
    app.run(
        host = conf['ip'], 
        debug = conf['debug'], 
        port = conf['port'], 
        use_reloader = conf['debug']
    )

if __name__ == '__main__':
    run()
