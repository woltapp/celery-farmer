from __future__ import absolute_import

import logging
import threading
import time
from itertools import chain

from farmer.broker import RedisBroker

logger = logging.getLogger(__name__)


class QueueLengths(threading.Thread):
    def __init__(self, celery_app, statsd_client, poll_time=1 * 10):
        super(QueueLengths, self).__init__()

        self.celery_app = celery_app
        self.statsd_client = statsd_client
        self.poll_time = poll_time

        self.is_terminated = False

        self.broker = RedisBroker(redis_uri=self.celery_app.broker_connection().as_uri())

    def stop(self):
        logger.info("Stopping QueueLengths")
        self.is_terminated = True

    def run(self):
        logger.info("Running QueueLengths")
        while not self.is_terminated:
            try:
                queues = self._get_active_queues()
                for queue_name in queues:
                    self._track_queue_length(queue_name)
            except Exception as e:
                logger.error("Failed to track queue lengths: %s", e)
            finally:
                poll_time = self.poll_time
                time.sleep(poll_time)

    def _get_active_queues(self):
        response = self.celery_app.control.inspect().active_queues()
        if response is None:
            return set()

        queues = [
            [queue["name"] for queue in node]
            for node in response.values()
        ]

        return set(chain(*queues))

    def _track_queue_length(self, queue_name):
        length = self.broker.get_queue_length(queue_name)
        tags = {'queue': queue_name}

        self.statsd_client.gauge("queues.length", length, tags=tags)
