from unittest.mock import Mock

from celery import Celery

from farmer.event_listener import EventListener
from tests import fixtures


def test_tracks_counts_of_events():
    statsd_mock = Mock()
    celery_app = Celery(broker='redis://localhost')
    listener = EventListener(celery_app, statsd_mock)

    listener.on_event(fixtures.task_received)
    assert statsd_mock.incr.called


def test_tracks_times():
    statsd_mock = Mock()
    celery_app = Celery(broker='redis://localhost')
    listener = EventListener(celery_app, statsd_mock)

    listener.on_event(fixtures.task_received)
    listener.on_event(fixtures.task_started)
    listener.on_event(fixtures.task_succeeded)

    assert statsd_mock.timing.call_count == 2
    assert statsd_mock.timing.call_args[0][0] == 'tasks.times.execution'
    assert statsd_mock.timing.call_args[0][1] > 0


def test_cleans_tracked_times():
    statsd_mock = Mock()
    celery_app = Celery(broker='redis://localhost')
    listener = EventListener(celery_app, statsd_mock)

    listener.on_event(fixtures.task_received)
    listener.on_event(fixtures.task_started)
    task_id = fixtures.task_received['uuid']
    assert listener.timings.get(task_id) is not None

    listener.on_event(fixtures.task_succeeded)
    assert listener.timings.get(task_id) is None
