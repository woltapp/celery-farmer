from __future__ import absolute_import

import logging
import threading
import time


logger = logging.getLogger(__name__)


class EnableEvents(threading.Thread):
    def __init__(self, celery_app, poll_time=1 * 10):
        super(EnableEvents, self).__init__()

        self.celery_app = celery_app
        self.poll_time = poll_time

        self.is_terminated = False

    def stop(self):
        logger.info('Stopping EnableEvents')
        self.is_terminated = True

    def run(self):
        logger.info('Running EnableEvents')
        while not self.is_terminated:
            logger.debug('Enabling events')
            try:
                self.celery_app.control.enable_events()
            finally:
                poll_time = self.poll_time
                time.sleep(poll_time)
