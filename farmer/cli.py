from __future__ import absolute_import

import sys
import os
import click


@click.group()
@click.version_option("0.1-alpha")
def cli():
    pass


@cli.command()
@click.option("--broker", "-b", help="Celery app's broker")
def start(broker):
    if not broker:
        raise click.BadParameter("Broker url is missing", param_hint="--broker")

    from farmer.application import Farmer
    farmer = Farmer(broker)
    farmer.start()


def _add_current_working_directory_to_path():
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    _add_current_working_directory_to_path()
    cli()
