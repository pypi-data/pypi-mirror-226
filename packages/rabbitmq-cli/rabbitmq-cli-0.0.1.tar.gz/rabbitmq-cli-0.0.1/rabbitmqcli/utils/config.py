import os

from configparser import ConfigParser
from functools import lru_cache


USER_CONFING_DIR = '{home}/.rabbitmq-cli'.format(home=os.path.expanduser('~'))
USER_CONFIG_FILE = '{cli_dir}/config'.format(cli_dir=USER_CONFING_DIR)


@lru_cache
def get_config() -> ConfigParser:
    config = ConfigParser()
    config.read(USER_CONFIG_FILE)

    if not config.sections():
        return _generate_config_file(config)

    return config

def _generate_config_file(config: ConfigParser):
    config.add_section('default')
    config['default']['hostname'] = 'localhost'
    config['default']['vhost'] = '/'
    config['default']['username'] = 'guest'
    config['default']['password'] = 'guest'
    config['default']['exchange'] = 'domainEvents'
    config['default']['queue'] = 'subsEvents'
    config['default']['credentials-from-secret'] = 'False'

    config.add_section('http')
    config['http']['port'] = '15671'
    config['http']['ssl'] = 'True'

    config.add_section('amqp')
    config['amqp']['port'] = '5671'
    config['amqp']['ssl'] = 'True'

    config.add_section('aws')
    config['aws']['region'] = 'us-east-1'
    config['aws']['secret-name'] = 'your-{env}-secret-name'

    if not os.path.isfile(USER_CONFIG_FILE):
        os.makedirs(USER_CONFING_DIR, exist_ok=True)

    with open(USER_CONFIG_FILE, 'w') as f:
        config.write(f)

    return config
