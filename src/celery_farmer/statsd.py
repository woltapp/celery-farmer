import logging
from typing import Any, Dict, Optional

import statsd

logger = logging.getLogger(__name__)


class StatsClient:

    def __init__(self, config: Dict[str, Any]) -> None:
        host = config.get('host', 'localhost')
        port = config.get('port', 8125)
        prefix = config.get('prefix', 'farmer')

        client = statsd.StatsClient(host, port, prefix=prefix)
        logger.info(
            f'Configuring StatsD, host: {host}, port: {port}, prefix: {prefix}'
        )
        self.client = client

    def timer(self, stat: str, tags: Optional[Dict[str, str]] = None,
              rate: int = 1) -> None:
        self.client.timer(self._get_stat(stat, tags), rate)

    def timing(self, stat: str, delta: float,
               tags: Optional[Dict[str, str]] = None, rate: int = 1) -> None:
        self.client.timing(self._get_stat(stat, tags), delta, rate)

    def incr(self, stat: str, count: int = 1,
             tags: Optional[Dict[str, str]] = None, rate: int = 1) -> None:
        self.client.incr(self._get_stat(stat, tags), count, rate)

    def decr(self, stat: str, count: int = 1,
             tags: Optional[Dict[str, str]] = None, rate: int = 1) -> None:
        self.client.decr(self._get_stat(stat, tags), count, rate)

    def gauge(self, stat: str, value: float, rate: int = 1,
              tags: Optional[Dict[str, str]] = None, delta: bool = False
              ) -> None:
        self.client.gauge(self._get_stat(stat, tags), value, rate, delta)

    def set(self, stat: str, value: float,
            tags: Optional[Dict[str, str]] = None, rate: int = 1) -> None:
        self.client.set(self._get_stat(stat, tags), value, rate)

    def _get_stat(self, stat: str, tags: Optional[Dict[str, str]]) -> str:
        if tags is not None:
            stat = f'{stat},{self._format_tags(tags)}'
        return stat

    def _format_tags(self, tags: Dict[str, str]) -> str:
        tag_pairs = (f'{k}={v}' for k, v in tags.items())
        return ','.join(tag_pairs)
