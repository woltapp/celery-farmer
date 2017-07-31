import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Farmer(object):
    def __init__(self, broker_url):
        self.broker_url = broker_url
        pass

    def start(self):
        logger.info("Starting Farmer with broker %s" % self.broker_url)
