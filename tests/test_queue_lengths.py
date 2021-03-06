from typing import Iterator
from unittest.mock import Mock, patch

from celery import Celery
from pytest import fixture

from celery_farmer.queue_lengths import QueueLengths
from tests import fixtures
from tests.helpers import wait_until_success


@fixture
def _queue_lengths(celery_app: Celery, statsd_mock: Mock
                   ) -> Iterator[QueueLengths]:
    queue_lengths = QueueLengths(
        celery_app,
        statsd_client=statsd_mock,
        poll_time=0.1,
    )

    queue_lengths.start()
    yield queue_lengths

    queue_lengths.stop()


@fixture
def _active_queues() -> Iterator[Mock]:
    with patch('celery.app.control.Inspect.active_queues') as active_queues:
        active_queues.return_value = fixtures.active_queues_response
        yield active_queues


def test_tracks_counts_of_events(_active_queues: Mock,
                                 _queue_lengths: QueueLengths,
                                 statsd_mock: Mock) -> None:
    def assert_mock_gauge_called() -> None:
        assert statsd_mock.gauge.called

    wait_until_success(assert_mock_gauge_called)


def test_sends_heartbeats(_active_queues: Mock, _queue_lengths: QueueLengths,
                          statsd_mock: Mock) -> None:
    def assert_mock_incr_called() -> None:
        assert statsd_mock.incr.called

    wait_until_success(assert_mock_incr_called)
    assert statsd_mock.incr.call_args[0][0] == 'heartbeats.queue_lengths'
