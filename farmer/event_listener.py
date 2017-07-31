from __future__ import absolute_import

import logging
import threading
import time

from celery.events import EventReceiver

logger = logging.getLogger(__name__)


class EventListener(threading.Thread):
    def __init__(self, celery_app):
        super(EventListener, self).__init__()
        self.daemon = True

        self.celery_app = celery_app
        self.state = self.celery_app.events.State()

    def run(self):
        logger.info("Running event listener")
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
        logger.debug("Got event %s", str(event))
