import unittest

from mock import Mock, patch

from celery import Celery

from farmer.queue_lengths import QueueLengths

from tests import fixtures
from tests.helpers.wait import wait_until_success


class QueueLengthsTestCase(unittest.TestCase):
    @patch('celery.app.control.Inspect.active_queues')
    def test_tracks_counts_of_events(self, active_queues):
        active_queues.return_value = fixtures.active_queues_response

        statsd_mock = Mock()
        queue_lengths = QueueLengths(
            Celery(broker="redis://localhost"),
            statsd_client=statsd_mock,
            poll_time=0.1,
        )
        try:
            queue_lengths.start()
            wait_until_success(lambda: self.assertTrue(statsd_mock.gauge.called))
        finally:
            queue_lengths.stop()
