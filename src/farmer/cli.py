from functools import partial
import os
import signal

import click

import farmer
from farmer.application import Farmer


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

    broker = os.getenv('BROKER', broker)
    poll_time = os.getenv('POLL_TIME', poll_time)
    statsd_host = os.getenv('STATSD_HOST', statsd_host)
    statsd_port = os.getenv('STATSD_PORT', statsd_port)
    statsd_prefix = os.getenv('STATSD_PREFIX', statsd_prefix)

    if not broker:
        raise click.BadParameter('Broker url is missing',
                                 param_hint='--broker')

    if poll_time:
        poll_time = int(poll_time)
    else:
        poll_time = 1 * 10

    farmer = Farmer(
        broker,
        poll_time,
        construct_statsd_configs(statsd_host, statsd_port, statsd_prefix)
    )
    farmer.start()

    signal.signal(signal.SIGINT, partial(stop_farmer, farmer))
    signal.pause()


if __name__ == '__main__':
    cli()
