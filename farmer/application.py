import logging

from celery import Celery

from farmer.enable_events import EnableEvents

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Farmer(object):
    def __init__(self, broker_url):
        self.broker_url = broker_url
        self.celery_app = Celery(broker=self.broker_url)

        self.enable_events_thread = EnableEvents(self.celery_app)

    def start(self):
        logger.info("Starting Farmer with broker %s" % self.broker_url)
        self.enable_events_thread.start()

    def stop(self):
        logger.info("Stopping farmer")
        self.enable_events_thread.stop()
