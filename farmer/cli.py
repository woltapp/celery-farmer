from __future__ import absolute_import

import click

from farmer.application import Farmer


@click.group()
@click.version_option("0.1-alpha")
def cli():
    pass


@cli.command()
@click.option("--broker", "-b", help="Celery app's broker")
def start(broker):
    if not broker:
        raise click.BadParameter("Broker url is missing", param_hint="--broker")

    farmer = Farmer(broker)
    farmer.start()


if __name__ == '__main__':
    cli()
