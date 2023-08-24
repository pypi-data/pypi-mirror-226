import atexit
import time
import requests

from requests.auth import HTTPBasicAuth
from .queues import _get_queue

from ..connection import get_connection
from ..utils import pprint, get_config


def publish_message(credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, routing_key: str, message: str, output: str):
    body = {
        'routing_key': routing_key,
        'payload': message,
        'payload_encoding': 'string',
        'properties': {}
    }
    response = requests.post(uri + '/{}/{}/publish'.format(vhost, exchange), auth=credentials, json=body)
    pprint(response, output)

def publishing(env: str, credentials: HTTPBasicAuth, uri: str, vhost: str, exchange: str, routing_key: str, queue: str, message: str, n: int, output: str):
    connection = get_connection(env, protocol='amqps')[1]
    channel = connection.channel()
    atexit.register(_close_connection, connection, channel)

    print('Press Crtl+D or Ctrl+C to exit... \n')
    config = get_config()

    if not queue:
        queue = config['default'].get('queue')

    uri = '/'.join(uri.split('/')[:-2])
    data = _get_queue(credentials, f'{uri}/api/queues', vhost, name=queue).json()
    channel.queue_declare(
        queue=queue,
        durable=data['durable'],
        arguments=data['arguments']
    )

    while True:
        for _ in range(n):
            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=message
            )

            if output:
                print('Message published!')

        time.sleep((1000 - (n * 10))/1000)

def _close_connection(connection, channel):
    print('Closing channel...')
    channel.close()
    print('Channel closed.')
    print('Closing channel...')
    connection.close()
    print('Connection closed.')
    print('\nGood bye!')
