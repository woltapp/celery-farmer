from unittest.mock import Mock

from celery import Celery
from pytest import fixture

from farmer.event_listener import EventListener
from tests import fixtures


@fixture(scope='function')
def _listener(celery_app: Celery, statsd_mock: Mock) -> EventListener:
    return EventListener(celery_app, statsd_mock)


def test_tracks_counts_of_events(_listener: EventListener, statsd_mock: Mock
                                 ) -> None:
    _listener.on_event(fixtures.task_received)
    assert statsd_mock.incr.called


def test_tracks_times(_listener: EventListener, statsd_mock: Mock) -> None:
    _listener.on_event(fixtures.task_received)
    _listener.on_event(fixtures.task_started)
    _listener.on_event(fixtures.task_succeeded)

    assert statsd_mock.timing.call_count == 2
    assert statsd_mock.timing.call_args[0][0] == 'tasks.times.execution'
    assert statsd_mock.timing.call_args[0][1] > 0


def test_cleans_tracked_times(_listener: EventListener) -> None:
    _listener.on_event(fixtures.task_received)
    _listener.on_event(fixtures.task_started)
    task_id = fixtures.task_received['uuid']
    assert _listener.timings.get(task_id) is not None

    _listener.on_event(fixtures.task_succeeded)
    assert _listener.timings.get(task_id) is None
