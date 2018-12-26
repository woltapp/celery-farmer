import unittest

from celery import Celery
from mock import patch

from farmer.enable_events import EnableEvents
from tests.helpers.wait import wait_until_success


class EnableEventsTestCase(unittest.TestCase):

    @patch('celery.app.control.Control.enable_events')
    def test_enabling_events(self, celery_enable_events):
        try:
            enable_events_thread = EnableEvents(
                Celery(broker='redis://localhost'),
                poll_time=0.1
            )
            enable_events_thread.start()
            wait_until_success(
                lambda: self.assertTrue(celery_enable_events.called))
        finally:
            enable_events_thread.stop()
