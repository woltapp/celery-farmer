from __future__ import absolute_import

import logging
import threading
import time


logger = logging.getLogger(__name__)


class EnableEvents(threading.Thread):
    def __init__(self, celery_app, poll_time=1 * 60):
        super(EnableEvents, self).__init__()

        self.celery_app = celery_app
        self.poll_time = poll_time

        self.is_terminated = False

    def stop(self):
        self.is_terminated = True

    def run(self):
        while not self.is_terminated:
            try:
                self.celery_app.control.enable_events()
            finally:
                poll_time = self.poll_time
                logger.debug("Sleeping for %i seconds before enabling events again" % poll_time)
                time.sleep(poll_time)
