from __future__ import absolute_import

import sys
import os
import signal
import click

from functools import partial

import farmer


@click.group()
@click.version_option(farmer.__version__)
def cli():
    pass


@cli.command()
@click.option('--broker', '-b', help="Celery app's broker url")
@click.option('--poll-time', help='Specify polling time')
@click.option('--statsd-host', '-sh', help='Statsd host')
@click.option('--statsd-port', '-sp', help='Statsd port')
@click.option('--statsd-prefix', '-spr', help='Statsd prefix')
def start(broker, poll_time, statsd_host, statsd_port, statsd_prefix):
    def stop_farmer(farmer, signal, frame):
        farmer.stop()

    def construct_statsd_configs(host, port, prefix):
        config = {}
        if host:
            config['host'] = host
        if port:
            config['port'] = int(port)
        if prefix:
            config['prefix'] = prefix
        return config

    broker = os.environ.get('BROKER', broker)
    poll_time = os.environ.get('POLL_TIME', poll_time)
    statsd_host = os.environ.get('STATSD_HOST', statsd_host)
    statsd_port = os.environ.get('STATSD_PORT', statsd_port)
    statsd_prefix = os.environ.get('STATSD_PREFIX', statsd_prefix)

    if not broker:
        raise click.BadParameter('Broker url is missing',
                                 param_hint='--broker')

    if poll_time:
        poll_time = int(poll_time)
    else:
        poll_time = 1 * 10

    from farmer.application import Farmer
    farmer = Farmer(
        broker,
        poll_time,
        construct_statsd_configs(statsd_host, statsd_port, statsd_prefix)
    )
    farmer.start()

    signal.signal(signal.SIGINT, partial(stop_farmer, farmer))
    signal.pause()


def _add_current_working_directory_to_path():
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    _add_current_working_directory_to_path()
    cli()
