import click

from requests import Response
from rich import print_json

from .. import __version__

from .config import get_config
from .secrets import get_secret


def pprint(response: Response, output: bool) -> None:
    print('{} [{}]: {}'.format(response.reason, response.status_code, response.url))

    if output:
        if response.text:
            click.echo('Response data: \n')
            print_json(data=response.json())

def version(f):
    """
    Add the version of the tool to the help heading.

    :param f: function to decorate
    :return: decorated function
    """
    doc = f.__doc__
    f.__doc__ = "Version: " + __version__ + "\n\n" + doc

    return f