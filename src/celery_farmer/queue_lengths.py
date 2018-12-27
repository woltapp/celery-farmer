from itertools import chain
import logging
import threading
import time
from typing import Set

from celery import Celery

from celery_farmer.broker import RedisBroker
from celery_farmer.statsd import StatsClient

logger = logging.getLogger(__name__)


class QueueLengths(threading.Thread):
    def __init__(self, celery_app: Celery, statsd_client: StatsClient,
                 poll_time: float = 10.0) -> None:
        super().__init__()

        self.celery_app = celery_app
        self.statsd_client = statsd_client
        self.poll_time = poll_time

        self.is_terminated = False

        self.broker = RedisBroker(
            redis_uri=self.celery_app.broker_connection().as_uri())

    def stop(self) -> None:
        logger.info('Stopping QueueLengths')
        self.is_terminated = True

    def run(self) -> None:
        logger.info('Running QueueLengths')
        while not self.is_terminated:
            logger.debug('Sending heart beat')
            self.statsd_client.incr('heartbeats.queue_lengths')
            try:
                queues = self._get_active_queues()
                for queue_name in queues:
                    self._track_queue_length(queue_name)
            except Exception as e:
                logger.error(f'Failed to track queue lengths: {e}')
            finally:
                poll_time = self.poll_time
                time.sleep(poll_time)

    def _get_active_queues(self) -> Set[str]:
        response = self.celery_app.control.inspect().active_queues()
        if response is None:
            return set()

        queues = [
            [queue['name'] for queue in node]
            for node in response.values()
        ]

        return set(chain(*queues))

    def _track_queue_length(self, queue_name: str) -> None:
        length = self.broker.get_queue_length(queue_name)
        tags = {'queue': queue_name}

        self.statsd_client.gauge('queues.length', length, tags=tags)
