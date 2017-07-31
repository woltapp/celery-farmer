from __future__ import absolute_import

import logging
import threading
import time

POLL_TIME = 1

logger = logging.getLogger(__name__)


class EnableEvents(threading.Thread):
    def __init__(self, celery_app):
        super(EnableEvents, self).__init__()

        self.celery_app = celery_app
        self.is_terminated = False

    def stop(self):
        self.is_terminated = True

    def run(self):
        while not self.is_terminated:
            try:
                self.celery_app.control.enable_events()
            finally:
                logger.debug("Sleeping for %i seconds before enabling events again" % POLL_TIME)
                time.sleep(POLL_TIME)
