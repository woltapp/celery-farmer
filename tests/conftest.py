from unittest.mock import Mock

from celery import Celery
from pytest import fixture


@fixture
def celery_app() -> Celery:
    return Celery(broker='redis://localhost')


@fixture(scope='function')
def statsd_mock() -> Mock:
    return Mock()
