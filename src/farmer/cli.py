from functools import partial
import signal

import click

import farmer
from farmer.application import Farmer


@click.group()
@click.version_option(farmer.__version__)
def cli():
    pass


@cli.command()
@click.option('--broker', '-b', envvar='BROKER', required=True,
              help="Celery app's broker url")
@click.option('--poll-time', envvar='POLL_TIME', type=float, default=10,
              help='Specify polling time')
@click.option('--statsd-host', '-sh', envvar='STASTD_HOST', help='Statsd host')
@click.option('--statsd-port', '-sp', envvar='STATSD_PORT', type=int,
              help='Statsd port')
@click.option('--statsd-prefix', '-spr', envvar='STATSD_PREFIX',
              help='Statsd prefix')
def start(broker, poll_time, statsd_host, statsd_port, statsd_prefix):
    def stop_farmer(farmer, signal, frame):
        farmer.stop()

    def construct_statsd_configs(host, port, prefix):
        config = {}
        if host:
            config['host'] = host
        if port:
            config['port'] = port
        if prefix:
            config['prefix'] = prefix
        return config

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
