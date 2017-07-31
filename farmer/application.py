import logging

import threading
import time

from celery import Celery

import control

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

ENABLE_EVENTS_POLL_TIME = 1


class Farmer(object):
    def __init__(self, broker_url):
        self.broker_url = broker_url
        self.celery_app = Celery(broker=self.broker_url)

        self.enable_events_thread = threading.Thread(target=self._enable_events)

    def start(self):
        logger.info("Starting Farmer with broker %s" % self.broker_url)
        self.enable_events_thread.start()

    def stop(self):
        logger.info("Stopping farmer")
        self.enable_events_thread.running = False

    def _enable_events(self):
        while getattr(threading.currentThread, "running", True):
            try:
                control.enable_events(self.celery_app)
            finally:
                logger.debug("Sleeping for %i seconds before enabling events again" % ENABLE_EVENTS_POLL_TIME)
                time.sleep(ENABLE_EVENTS_POLL_TIME)
