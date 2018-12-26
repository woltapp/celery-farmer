from typing import Iterator
from unittest.mock import Mock, patch

from celery import Celery
from pytest import fixture

from farmer.enable_events import EnableEvents
from tests.helpers import wait_until_success


@fixture
def _enable_events_thread(celery_app: Celery) -> Iterator[EnableEvents]:
    enable_events_thread = EnableEvents(celery_app, poll_time=0.1)
    enable_events_thread.start()

    yield enable_events_thread
    enable_events_thread.stop()


@patch('celery.app.control.Control.enable_events')
def test_enabling_events(celery_enable_events: Mock,
                         _enable_events_thread: EnableEvents) -> None:
    def assert_enable_called() -> None:
        assert celery_enable_events.called

    wait_until_success(assert_enable_called)
