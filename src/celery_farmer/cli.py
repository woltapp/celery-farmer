from functools import partial
from inspect import FrameInfo
import signal
from typing import Any, Dict

import click

import celery_farmer
from celery_farmer.application import Farmer


@click.group()
@click.version_option(celery_farmer.__version__)
def cli() -> None:
    pass


@cli.command()
@click.option('--broker', '-b', envvar='BROKER', required=True,
              help="Celery app's broker url")
@click.option('--poll-time', envvar='POLL_TIME', type=float, default=10,
              help='Specify polling time')
@click.option('--statsd-host', '-sh', envvar='STATSD_HOST', help='Statsd host')
@click.option('--statsd-port', '-sp', envvar='STATSD_PORT', type=int,
              help='Statsd port')
@click.option('--statsd-prefix', '-spr', envvar='STATSD_PREFIX',
              help='Statsd prefix')
def start(broker: str, poll_time: float, statsd_host: str, statsd_port: int,
          statsd_prefix: str) -> None:
    def stop_farmer(farmer: Farmer, signal: int, frame: FrameInfo) -> None:
        farmer.stop()

    def construct_statsd_configs(host: str, port: int, prefix: str
                                 ) -> Dict[str, Any]:
        config: Dict[str, Any] = {}
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
