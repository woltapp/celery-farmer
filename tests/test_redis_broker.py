import unittest

from farmer.broker import RedisBroker


class RedisBrokerTestCase(unittest.TestCase):
    def test_parses_full_uri(self):
        self.assertIsNotNone(RedisBroker("redis://localhost:6379/1/"))

    def test_parses_uri_without_database(self):
        self.assertIsNotNone(RedisBroker("redis://localhost:6379//"))
