from unittest.mock import patch

from pytest import fixture

from farmer.enable_events import EnableEvents
from tests.helpers import wait_until_success


@fixture
def _enable_events_thread(celery_app):
    enable_events_thread = EnableEvents(celery_app, poll_time=0.1)
    enable_events_thread.start()

    yield enable_events_thread
    enable_events_thread.stop()


@patch('celery.app.control.Control.enable_events')
def test_enabling_events(celery_enable_events, _enable_events_thread):
    def assert_enable_called():
        assert celery_enable_events.called

    wait_until_success(assert_enable_called)
