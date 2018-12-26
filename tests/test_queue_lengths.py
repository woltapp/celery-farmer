from unittest.mock import patch

from pytest import fixture

from farmer.queue_lengths import QueueLengths
from tests import fixtures
from tests.helpers import wait_until_success


@fixture
def _queue_lengths(celery_app, statsd_mock):
    queue_lengths = QueueLengths(
        celery_app,
        statsd_client=statsd_mock,
        poll_time=0.1,
    )

    queue_lengths.start()
    yield queue_lengths

    queue_lengths.stop()


@fixture
def _active_queues():
    with patch('celery.app.control.Inspect.active_queues') as active_queues:
        active_queues.return_value = fixtures.active_queues_response
        yield active_queues


def test_tracks_counts_of_events(_active_queues, _queue_lengths, statsd_mock):
    def assert_mock_gauge_called():
        assert statsd_mock.gauge.called

    wait_until_success(assert_mock_gauge_called)


def test_sends_heartbeats(_active_queues, _queue_lengths, statsd_mock):
    def assert_mock_incr_called():
        assert statsd_mock.incr.called

    wait_until_success(assert_mock_incr_called)
    assert statsd_mock.incr.call_args[0][0] == 'heartbeats.queue_lengths'
