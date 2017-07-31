from __future__ import absolute_import

import unittest
from mock import patch
from click.testing import CliRunner

from farmer.cli import cli


class CLITestCase(unittest.TestCase):
    def test_start_gives_error_if_broker_is_missing(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['start'])
        self.assertTrue(result.exit_code > 0)
        self.assertIn("Invalid value for --broker", result.output)

    @patch('farmer.application.Farmer.start')
    def test_starts_farmer(self, start_patch):
        runner = CliRunner()
        result = runner.invoke(cli, ['start', '--broker', 'redis://localhost'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(start_patch.call_count, 1)
