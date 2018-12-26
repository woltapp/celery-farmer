from unittest.mock import patch

from celery import Celery

from farmer.enable_events import EnableEvents
from tests.helpers import wait_until_success


@patch('celery.app.control.Control.enable_events')
def test_enabling_events(celery_enable_events):
    try:
        enable_events_thread = EnableEvents(
            Celery(broker='redis://localhost'),
            poll_time=0.1
        )
        enable_events_thread.start()

        def assert_enable_called():
            assert celery_enable_events.called

        wait_until_success(assert_enable_called)
    finally:
        enable_events_thread.stop()
