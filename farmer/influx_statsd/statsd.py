from __future__ import absolute_import

import logging

import statsd

logger = logging.getLogger(__name__)


class InfluxDStatsDClient(object):

    def __init__(self):
        self.client = None

    def init_app(self, host='localhost', port=8125, prefix="farmer"):
        client = statsd.StatsClient(host, port, prefix=prefix)
        logger.info('Configuring StatsD', extra={'statsd_port': port,
                                                 'statsd_host': host,
                                                 'statsd_prefix': prefix})
        self.client = client

    def timer(self, stat, tags=None, rate=1):  # pragma: no coverage
        self.client.timer(self._get_stat(stat, tags), rate)

    def timing(self, stat, delta, tags=None, rate=1):
        self.client.timing(self._get_stat(stat, tags), delta, rate)

    def incr(self, stat, count=1, tags=None, rate=1):
        self.client.incr(self._get_stat(stat, tags), count, rate)

    def decr(self, stat, count=1, tags=None, rate=1):  # pragma: no coverage
        self.client.decr(self._get_stat(stat, tags), count, rate)

    def gauge(self, stat, value, rate=1, tags=None, delta=False):  # pragma: no coverage
        self.client.gauge(self._get_stat(stat, tags), value, rate, delta)

    def set(self, stat, value, tags=None, rate=1):  # pragma: no coverage
        self.client.set(self._get_stat(stat, tags), value, rate)

    def _get_stat(self, stat, tags):
        if tags:
            stat = '%s,%s' % (stat, self._format_tags(tags))
        return stat

    def _format_tags(self, tags):
        tag_pairs = ['%s=%s' % (k, v) for k, v in tags.items()]
        return ','.join(tag_pairs)
