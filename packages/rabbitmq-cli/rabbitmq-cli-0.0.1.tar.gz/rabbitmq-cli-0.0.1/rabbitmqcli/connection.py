import pika
import ssl

from configparser import ConfigParser
from functools import lru_cache
from requests.auth import HTTPBasicAuth
from urllib.parse import quote_plus

from .utils import get_config
from .utils import get_secret


@lru_cache
def get_connection(env, protocol='https'):
    config = get_config()
    username, password = _get_credentials(config, env)
    hostname = config['default'].get('hostname')
    vhost = config['default'].get('vhost')

    if protocol == 'https':
        credentials = HTTPBasicAuth(username, password)
        endpoint = '{protocol}://{hostname}:{port}'.format(
            protocol='https' if config['http'].getboolean('ssl') else 'http',
            hostname=hostname,
            port=config['http'].getint('port')
        )
        return credentials, endpoint, quote_plus(vhost)

    elif protocol == 'amqps':
        credentials = pika.PlainCredentials(username, password)
        ssl_context = None

        if config['amqp'].getboolean('ssl'):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

        params = pika.ConnectionParameters(
            host=hostname,
            port=5671,
            credentials=credentials,
            ssl_options=pika.SSLOptions(context=ssl_context),
            client_properties={
                'connection_name': 'RabbitMQ Custom CLI'
            }
        )
        connection = pika.BlockingConnection(params)
        return credentials, connection, vhost

    raise RuntimeError('Protocol must be defined')

def _get_credentials(config: ConfigParser, env: str) -> tuple:
    use_secret = config['default'].get('credentials-from-secret')

    if not use_secret:
        username = config['default'].get('username')
        password = config['default'].get('password')

        if not (username and password):
            raise Exception('Define credentilas on config file or enable get credentials from secret')
    else:
        try:
            secret_name = config['aws'].get('secret-name').format(env=env)
        except KeyError:
            print('\nError getting credentials from secret. If you are using a composed name check that key must be "env"!')
            exit()

        region = config['aws'].get('region')
        value = get_secret(secret_name, region)

        try:
            username = value['username']
            password = value['password']
        except KeyError:
            print('\nError getting credentials from secret. Check secret structure!')
            exit()

    return username, password
