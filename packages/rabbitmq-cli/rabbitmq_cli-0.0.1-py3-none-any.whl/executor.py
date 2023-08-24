import sys
import click

from urllib.parse import quote_plus

from rabbitmqcli import __version__
from rabbitmqcli.connection import get_connection
from rabbitmqcli.utils import version, get_config


ENV_OPTION_ARGS = ('-e', '--env', 'env')
ENV_OPTION_KWARGS = {'help': 'Set environment for RabbitMQ connection.', 'type': click.Choice(['dev', 'qa'], case_sensitive=False), 'default': 'dev'}

OUT_OPTION_ARGS = ('-o', '--output', 'output')
OUT_OPTION_KWARGS = {'help': 'Show output details.', 'is_flag': True}

@click.group()
@click.version_option(
    __version__, '-v', '--version', message='%(prog)s, version %(version)s'
)
@version
def cli():
    '''RabbitMQ CLI

    With tens of thousands of users, RabbitMQ is one of the most popular open source message brokers.
    From T-Mobile to Runtastic, RabbitMQ is used worldwide at small startups and large enterprises.

    This program allows to connect to a RabbitMQ Broker setting up dev and qa environments and excute
    some actions. This project is external to official project and official CLIs like:
    
    * rabbitmqctl: for service management and general operator tasks.

    * rabbitmq-diagnostics: for diagnostics and health checking.

    * rabbitmq-plugins: for plugin management.

    * rabbitmq-queues: for maintenance tasks on queues, in particular quorum queues.

    * rabbitmq-streams: for maintenance tasks on streams.
    
    * rabbitmq-upgrade: for maintenance tasks related to upgrades.

    https://www.rabbitmq.com
    '''
    pass

@cli.command()
@click.option(*ENV_OPTION_ARGS, **ENV_OPTION_KWARGS)
@click.option('-l', '--list', 'list_', is_flag=True, help='A list of all vhosts.')
@click.option('-n', '--name', 'name', type=str, help='An individual virtual host. As a virtual host usually only has a name, you do not need an HTTP body when PUTing one of these.')
@click.option(*OUT_OPTION_ARGS, **OUT_OPTION_KWARGS)
def vhosts(env, list_, name, output):
    ''' Virtual Hosts

    RabbitMQ is multi-tenant system: connections, exchanges, queues, bindings, user permissions, policies and
    some other things belong to virtual hosts, logical groups of entities. If you are familiar with virtual
    hosts in Apache or server blocks in Nginx, the idea is similar.

    There is, however, one important difference: virtual hosts in Apache are defined in the configuration file;
    that's not the case with RabbitMQ: virtual hosts are created and deleted using rabbitmqctl or the HTTP
    API instead.

    https://www.rabbitmq.com/vhosts.html
    '''
    from rabbitmqcli.modules.vhosts import list_vhosts, get_vhost

    credentials, uri, vhost = _get_(env, 'api/vhosts')

    if list_:
        list_vhosts(credentials, uri, output)
    elif name:
        get_vhost(credentials, uri, vhost, output)

@cli.command()
@click.option(*ENV_OPTION_ARGS, **ENV_OPTION_KWARGS)
@click.option('-l', '--list', 'list_', is_flag=True, help='A list of all queues.')
@click.option('-lv', '--list-by-vhost', 'vhost', type=str, help='A list of all queues in a given virtual host.')
@click.option('-n', '--name', 'name', type=str, help='An individual queue.')
@click.option(*OUT_OPTION_ARGS, **OUT_OPTION_KWARGS)
def queues(env, list_, vhost, name, output):
    ''' Queues

    A queue is a sequential data structure with two primary operations: an item can be enqueued (added) at the tail
    and dequeued (consumed) from the head. Queues play a prominent role in the messaging technology space: many
    messaging protocols and tools assume that publishers and consumers communicate using a queue-like storage mechanism.

    Queues in RabbitMQ are FIFO ("first in, first out"). Some queue features, namely priorities and requeueing by consumers,
    can affect the ordering as observed by consumers.

    https://www.rabbitmq.com/queues.html
    '''
    from rabbitmqcli.modules.queues import list_queues, list_vhost_queues, get_queue

    credentials, uri, default_vhost = _get_(env, 'api/queues')

    if list_:
        list_queues(credentials, uri, output)
    elif vhost:
        list_vhost_queues(credentials, uri, quote_plus(vhost), output)
    elif name:
        get_queue(credentials, uri, vhost, output)

@cli.command()
@click.option(*ENV_OPTION_ARGS, **ENV_OPTION_KWARGS)
@click.option('-l', '--list', 'list_', is_flag=True, help='An individual binding between an exchange and a queue. The props part of the URI is a "name" for the binding composed of its routing key and a hash of its arguments. props is the field named "properties_key" from a bindings listing response.')
@click.option('-v', '--vhost', 'vhost', type=str, required=True, help='Set virtual host')
@click.option('-e', '--exchange', 'exchange', type=str, required=True, help='Set exchange')
@click.option('-q', '--queue', 'queue', type=str, required=True, help='Set queue.')
@click.option('-rk', '--routing-key', 'routing_key', type=str, help='Set routing key.')
@click.option('-a', '--args', 'args', type=dict, default={}, help='Binding arguments.')
@click.option('--create', 'create', type=str, help='Remember, an exchange and a queue can be bound together many times! Request body should be a JSON object optionally containing two fields, routing_key (a string) and arguments (a map of optional arguments).')
@click.option('--delete', 'delete', type=str, help='An individual binding between an exchange and a queue. The props part of the URI is a "name" for the binding composed of its routing key and a hash of its arguments. props is the field named "properties_key" from a bindings listing response.')
@click.option('--bulk', 'bulk', type=str, help='Bulk create 2000 bindings for predefined exchange and queue.')
@click.option(*OUT_OPTION_ARGS, **OUT_OPTION_KWARGS)
def bindings(env, list_, vhost, exchange, queue, routing_key, args, create, delete, bulk, output):
    ''' Bindings

    A binding is a relationship between an exchange and a queue. This can be simply read as: the queue is interested in
    messages from this exchange.

    Bindings can take an extra routing_key parameter. To avoid the confusion with a basic_publish parameter we're going
    to call it a binding key.

    https://www.rabbitmq.com/tutorials/tutorial-four-python.html
    '''
    from rabbitmqcli.modules.bindings import list_bindings, get_binding, create_binding, delete_binding, bulk_bindings

    credentials, uri, default_vhost = _get_(env, 'api/bindings')
    vhost = quote_plus(vhost)

    if list_:
        list_bindings(credentials, uri, vhost, exchange, queue, output)
    elif create and routing_key:
        create_binding(credentials, uri, vhost, exchange, queue, routing_key, args, output)
    elif delete and routing_key:
        delete_binding(credentials, uri, vhost, exchange, queue, routing_key, args, output)
    elif bulk and routing_key:
        bulk_bindings(credentials, uri, vhost, exchange, queue, routing_key, args, output)
    elif routing_key:
        get_binding(credentials, uri, vhost, exchange, queue, routing_key, output)

@cli.command()
@click.option(*ENV_OPTION_ARGS, **ENV_OPTION_KWARGS)
@click.option('-v', '--vhost', 'vhost', type=str, required=True, help='Set virtual host.')
@click.option('-e', '--exchange', 'exchange', type=str, help='Set exchange.')
@click.option('-rk', '--routing-key', 'routing_key', type=str, required=True, help='Set routing key.')
@click.option('-m', '--message', 'message', type=str, required=True, help='Set message.')
@click.option('-q', '--queue', 'queue', type=str, help='Set queue.')
@click.option('-t', '--threads', 'threads', type=int, default=4, help='Set number of threads.')
@click.option('-c', '--constantly', 'constantly', is_flag=True, help='Publish a message to a given exchange constantly.')
@click.option(*OUT_OPTION_ARGS, **OUT_OPTION_KWARGS)
def publisher(env, vhost, exchange, routing_key, message, queue, constantly, threads, output):
    ''' Publisher

    Publish a message to a given exchange.
    '''
    from rabbitmqcli.modules.exchanges import publish_message, publishing

    credentials, uri, vhost = _get_(env, 'api/exchanges')
    config = get_config()

    if not exchange:
        exchange = config['default'].get('exchange')

    if vhost and routing_key and message and constantly:
        publishing(env, credentials, uri, vhost, exchange, routing_key, queue, message, threads, output)
    elif vhost and routing_key and message:
        publish_message(credentials, uri, vhost, exchange, routing_key, message, output)


def _get_(env, path):
    credentials, endpoint, vhost = get_connection(env)
    uri = '{endpoint}/{path}'.format(endpoint=endpoint, path=path)

    return credentials, uri, vhost

# if args.output:
#     print('\nValues defined by user... \n')
#     print('Queue: {}'.format(QUEUE))
#     print('Exchange: {}'.format(EXCHANGE))
#     print('Environment: {}\n'.format(args.env))

if __name__ == '__main__':
    cli()
