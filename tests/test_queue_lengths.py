import unittest

from mock import Mock, patch

from celery import Celery

from farmer.queue_lengths import QueueLengths

from tests import fixtures
from tests.helpers.wait import wait_until_success


@patch('celery.app.control.Inspect.active_queues')
class QueueLengthsTestCase(unittest.TestCase):

    def setUp(self):
        self.statsd_mock = Mock()
        self.queue_lengths = QueueLengths(
            Celery(broker='redis://localhost'),
            statsd_client=self.statsd_mock,
            poll_time=0.1,
        )

    def test_tracks_counts_of_events(self, active_queues):
        active_queues.return_value = fixtures.active_queues_response

        try:
            self.queue_lengths.start()
            wait_until_success(lambda: self.assertTrue(self.statsd_mock.gauge.called))
        finally:
            self.queue_lengths.stop()

    def test_sends_heartbeats(self, active_queues):
        active_queues.return_value = fixtures.active_queues_response

        try:
            self.queue_lengths.start()
            wait_until_success(
                lambda: self.assertTrue(self.statsd_mock.incr.called))
            self.assertEqual(self.statsd_mock.incr.call_args[0][0],
                             'heartbeats.queue_lengths')
        finally:
            self.queue_lengths.stop()
