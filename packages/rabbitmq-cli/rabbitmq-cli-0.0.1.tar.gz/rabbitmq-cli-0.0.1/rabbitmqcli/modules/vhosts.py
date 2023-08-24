import requests

from requests.auth import HTTPBasicAuth

from ..utils import pprint


def list_vhosts(credentials: HTTPBasicAuth, uri: str, output: bool):
    response = requests.get(uri, auth=credentials)
    pprint(response, output)

def get_vhost(credentials: HTTPBasicAuth, uri: str, name: str, output: bool):
    url = '{uri}/{vhost}'.format(uri=uri, vhost=name)
    response = requests.get(url, auth=credentials)
    pprint(response, output)
