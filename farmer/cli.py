from __future__ import absolute_import

import sys
import os
import signal
import click

from functools import partial


@click.group()
@click.version_option("0.1-alpha")
def cli():
    pass


@cli.command()
@click.option("--broker", "-b", help="Celery app's broker")
@click.option("--poll-time", help="Specify polling time")
@click.option("--statsd-host", "-sh", help="Statsd host")
@click.option("--statsd-port", "-sp", help="Statsd port")
@click.option("--statsd-prefix", "-spr", help="Statsd prefix")
def start(broker, poll_time, statsd_host, statsd_port, statsd_prefix):
    def stop_farmer(farmer, signal, frame):
        farmer.stop()

    def construct_statsd_configs():
        config = {}
        if statsd_host:
            config["host"] = statsd_host
        if statsd_port:
            config["port"] = statsd_port
        if statsd_prefix:
            config["prefix"] = statsd_prefix
        return config

    if not broker:
        raise click.BadParameter("Broker url is missing", param_hint="--broker")

    if poll_time:
        poll_time = int(poll_time)
    else:
        poll_time = 1 * 10

    from farmer.application import Farmer
    farmer = Farmer(broker, poll_time, construct_statsd_configs())
    farmer.start()

    signal.signal(signal.SIGINT, partial(stop_farmer, farmer))
    signal.pause()


def _add_current_working_directory_to_path():
    sys.path.append(os.getcwd())


if __name__ == '__main__':
    _add_current_working_directory_to_path()
    cli()
