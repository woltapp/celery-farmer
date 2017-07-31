import logging

from celery import Celery

from farmer.enable_events import EnableEvents
from farmer.event_listener import EventListener

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Farmer(object):
    def __init__(self, broker_url, poll_time):
        self.broker_url = broker_url
        self.celery_app = Celery(broker=self.broker_url)

        self.enable_events_thread = EnableEvents(self.celery_app, poll_time)
        self.event_listener_thread = EventListener(self.celery_app)

    def start(self):
        logger.info("Starting Farmer with broker %s" % self.broker_url)
        self.enable_events_thread.start()
        self.event_listener_thread.start()

    def stop(self):
        logger.info("Stopping farmer")
        self.enable_events_thread.stop()
