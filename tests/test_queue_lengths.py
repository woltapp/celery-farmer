from unittest.mock import Mock, patch

from celery import Celery

from farmer.queue_lengths import QueueLengths
from tests import fixtures
from tests.helpers import wait_until_success


@patch('celery.app.control.Inspect.active_queues')
def test_tracks_counts_of_events(active_queues):
    active_queues.return_value = fixtures.active_queues_response
    statsd_mock = Mock()
    queue_lengths = QueueLengths(
        Celery(broker='redis://localhost'),
        statsd_client=statsd_mock,
        poll_time=0.1,
    )

    try:
        queue_lengths.start()

        def assert_mock_gauge_called():
            assert statsd_mock.gauge.called

        wait_until_success(assert_mock_gauge_called)
    finally:
        queue_lengths.stop()


@patch('celery.app.control.Inspect.active_queues')
def test_sends_heartbeats(active_queues):
    active_queues.return_value = fixtures.active_queues_response
    statsd_mock = Mock()
    queue_lengths = QueueLengths(
        Celery(broker='redis://localhost'),
        statsd_client=statsd_mock,
        poll_time=0.1,
    )

    try:
        queue_lengths.start()

        def assert_mock_incr_called():
            assert statsd_mock.incr.called

        wait_until_success(assert_mock_incr_called)
        assert statsd_mock.incr.call_args[0][0] == 'heartbeats.queue_lengths'
    finally:
        queue_lengths.stop()
