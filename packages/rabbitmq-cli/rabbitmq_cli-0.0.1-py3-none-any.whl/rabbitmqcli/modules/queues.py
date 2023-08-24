import requests

from requests import Response
from requests.auth import HTTPBasicAuth

from ..utils import pprint, get_config


def list_queues(credentials: HTTPBasicAuth, uri: str, output: bool) -> None:
    response = requests.get(uri, auth=credentials)
    pprint(response, output)

def list_vhost_queues(credentials: HTTPBasicAuth, uri: str, vhost: str, output: bool) -> None:
    response = requests.get(f'{uri}/{vhost}', auth=credentials)
    pprint(response, output)

def _get_queue(credentials: HTTPBasicAuth, uri: str, vhost: str, name: str) -> Response:
    return requests.get(f'{uri}/{vhost}/{name}', auth=credentials)

def get_queue(credentials: HTTPBasicAuth, uri: str, vhost: str, name: str, output: bool) -> None:
    if not name:
        config = get_config()
        name = config['default'].get('queue')

    response = _get_queue(credentials, uri, vhost, name)
    pprint(response, output)
