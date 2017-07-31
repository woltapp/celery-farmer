import unittest

from mock import Mock

from celery import Celery

from farmer.event_listener import EventListener

from tests import fixtures


class EventListenerTestCase(unittest.TestCase):
    def test_tracks_counts_of_events(self):
        statsd_mock = Mock()
        celery_app = Celery(broker="redis://localhost")
        listener = EventListener(celery_app, statsd_mock)

        listener.on_event(fixtures.task_received)
        self.assertTrue(statsd_mock.incr.called)

    def test_tracks_times(self):
        statsd_mock = Mock()
        celery_app = Celery(broker="redis://localhost")
        listener = EventListener(celery_app, statsd_mock)

        listener.on_event(fixtures.task_received)
        listener.on_event(fixtures.task_started)
        listener.on_event(fixtures.task_succeeded)

        self.assertEqual(statsd_mock.timing.call_count, 2)
        self.assertEqual(statsd_mock.timing.call_args[0][0], "times.execution")
        self.assertGreater(statsd_mock.timing.call_args[0][1], 0)
