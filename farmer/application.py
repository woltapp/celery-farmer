import logging

from celery import Celery

from farmer.enable_events import EnableEvents
from farmer.event_listener import EventListener
from farmer.queue_lengths import QueueLengths
from farmer.influx_statsd.statsd import InfluxDStatsDClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

logger = logging.getLogger(__name__)


class Farmer:
    def __init__(self, broker_url, poll_time, statsd_config):
        self.broker_url = broker_url
        self.celery_app = Celery(broker=self.broker_url)

        self.statsd_client = InfluxDStatsDClient(statsd_config)

        self.enable_events_thread = EnableEvents(self.celery_app, poll_time)
        self.queue_lenghts_thread = QueueLengths(self.celery_app,
                                                 self.statsd_client, poll_time)

        self.event_listener_thread = EventListener(self.celery_app,
                                                   self.statsd_client)

    def start(self):
        logger.info(f'Starting Farmer with broker {self.broker_url}')
        self.enable_events_thread.start()
        self.queue_lenghts_thread.start()

        self.event_listener_thread.start()

    def stop(self):
        logger.info('Stopping farmer')
        self.enable_events_thread.stop()
        self.queue_lenghts_thread.stop()
