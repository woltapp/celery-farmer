import logging
import threading
import time
from typing import Any, Dict

from celery import Celery
from celery.events import EventReceiver
from celery.events.state import State

from celery_farmer.statsd import StatsClient
from celery_farmer.task import get_tags

logger = logging.getLogger(__name__)


class EventListener(threading.Thread):
    def __init__(self, celery_app: Celery, statsd_client: StatsClient) -> None:
        super().__init__()
        self.daemon = True

        self.celery_app = celery_app
        self.state = self.celery_app.events.State()
        self.statsd_client = statsd_client

        self.is_terminated = False

        self.timings: Dict[str, Dict[str, Any]] = {}

    def stop(self) -> None:
        logger.info('Stopping EventListener')
        self.is_terminated = True

    def run(self) -> None:
        logger.info(f'Running EventListener with daemon: {self.isDaemon()}')
        sleep_time = 1
        while not self.is_terminated:
            try:
                if sleep_time < 10:
                    sleep_time *= 2

                with self.celery_app.connection() as connection:
                    receiver = EventReceiver(
                        connection,
                        handlers={'*': self.on_event},
                        app=self.celery_app
                    )
                    sleep_time = 1
                    receiver.capture(limit=None, timeout=None, wakeup=True)
            except Exception as e:
                logger.debug(e, exc_info=True)
                logger.error(f'Failed to capture events: {e}')
                time.sleep(sleep_time)

    def on_event(self, event: Dict[str, Any]) -> None:
        if event['type'].startswith('task-'):
            logger.debug(f'Got event {event}')

            self.state.event(event)
            task = self.state.tasks.get(event['uuid'])

            self.track_event(task)
            self.track_timing(task)

    def track_event(self, task: State.Task) -> None:
        task_tags = get_tags(task)
        self.statsd_client.incr(f'tasks.counts.{task.type}', tags=task_tags)

    def track_timing(self, task: State.Task) -> None:
        now = time.time()
        task_timings = self.timings.get(task.uuid, {})
        task_tags = get_tags(task)

        if task.type == 'task-received':
            task_timings['received'] = now
        elif task.type == 'task-started':
            task_timings['started'] = now

            time_received = task_timings.get('received')
            if time_received:
                time_not_started = now - time_received
                self.statsd_client.timing(
                    'tasks.times.not_started',
                    time_not_started * 1000,
                    tags=task_tags
                )
            else:
                logger.error(f"Task {task.uuid} didn't have received time")
        elif task.type == 'task-succeeded' or task.type == 'task-failed':
            time_started = task_timings.get('started')
            if time_started:
                execution_time = now - time_started
                self.statsd_client.timing(
                    'tasks.times.execution',
                    execution_time * 1000,
                    tags=task_tags
                )
            else:
                logger.error(f"Task {task.uuid} didn't have started time")

            task_timings = {}

        if len(task_timings) > 0:
            self.timings[task.uuid] = task_timings
        elif self.timings.get(task.uuid):
            del self.timings[task.uuid]
