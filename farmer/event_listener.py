from __future__ import absolute_import

import logging
import threading
import time

from celery.events import EventReceiver

from farmer.task import get_tags

logger = logging.getLogger(__name__)


class EventListener(threading.Thread):
    def __init__(self, celery_app, statsd_client):
        super(EventListener, self).__init__()
        self.daemon = True

        self.celery_app = celery_app
        self.state = self.celery_app.events.State()
        self.statsd_client = statsd_client

        self.timings = {}

    def run(self):
        logger.info("Running EventListener")
        try_interval = 1
        while True:
            try:
                if try_interval < 10:
                    try_interval *= 2

                with self.celery_app.connection() as connection:
                    receiver = EventReceiver(
                        connection,
                        handlers={"*": self.on_event},
                        app=self.celery_app
                    )
                    try_interval = 1
                    receiver.capture(limit=None, timeout=None, wakeup=True)
            except Exception as e:
                logger.debug(e, exc_info=True)
                logger.error("Failed to capture events: %s", e)
                time.sleep(try_interval)

    def on_event(self, event):
        if event["type"].startswith("task-"):
            logger.debug("Got event %s", str(event))

            self.state.event(event)
            task = self.state.tasks.get(event["uuid"])

            self.track_event(task)
            self.track_timing(task)

    def track_event(self, task):
        task_tags = get_tags(task)
        self.statsd_client.incr("count.%s" % task.type, tags=task_tags)

    def track_timing(self, task):
        now = time.time()
        task_timings = self.timings.get(task.uuid, {})
        task_tags = get_tags(task)

        if task.type == "task-received":
            task_timings["received"] = now
        elif task.type == "task-started":
            task_timings["started"] = now

            time_received = task_timings.get("received")
            if time_received:
                time_in_queue = now - time_received
                self.statsd_client.timing("times.in_queue", time_in_queue * 1000, tags=task_tags)
            else:
                logger.error("Task %s didn't have received time" % task.uuid)
        elif task.type == "task-succeeded" or task.type == "task-failed":
            time_started = task_timings.get("started")
            if time_started:
                execution_time = now - time_started
                self.statsd_client.timing("times.execution", execution_time * 1000, tags=task_tags)
            else:
                logger.error("Task %s didn't have started time" % task.uuid)

            task_timings = {}

        if len(task_timings) > 0:
            self.timings[task.uuid] = task_timings
        elif self.timings.get(task.uuid):
            del self.timings[task.uuid]
