import requests

from requests.auth import HTTPBasicAuth

from ..utils import pprint, get_config

config = get_config()


def _path(vhost: str, exchange: str, queue: str) -> str:
    if not vhost:
        vhost = config['default'].get('vhost')

    if not exchange:
        exchange = config['default'].get('exchange')

    if not queue:
        queue = config['default'].get('queue')

    return f'/{vhost}/e/{exchange}/q/{queue}'

def list_bindings(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, queue: str, output: str) -> None:
    path = _path(vhost, exchange, queue)
    response = requests.get(uri + path, auth=credentials)
    pprint(response, output)

def _url(uri: str, vhost: str, exchange: str, queue: str, routing_key: str) -> str:
    return uri + _path(vhost, exchange, queue) + f'/{routing_key}'

def get_binding(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, queue: str, routing_key: str, output: str) -> None:
    response = requests.get(_url(uri, vhost, exchange, queue, routing_key), auth=credentials)
    pprint(response, output)

def delete_binding(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, queue: str, routing_key: str, args: dict, output: str) -> None:
    response = requests.delete(_url(uri, vhost, exchange, queue, routing_key), auth=credentials)
    pprint(response, output)

def create_binding(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, queue: str, routing_key: str, args: dict, output: str) -> None:
    path = _path(vhost, exchange, queue)
    body = {'routing_key': routing_key, 'arguments': args}
    response = requests.post(uri + path, auth=credentials, json=body)
    pprint(response, output)

def bulk_bindings(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, queue: str, routing_key: str, args: dict, output: str) -> None:
    path = _path(vhost, exchange, queue)

    for index in range(1, 2001):
        body = {'routing_key': f'{routing_key}.{index}', 'arguments': args}
        response = requests.post(uri + path, auth=credentials, json=body)

        if output:
            print('[{}] {}'.format(response.status_code, routing_key))
