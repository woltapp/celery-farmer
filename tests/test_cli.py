import unittest
from unittest.mock import patch

from click.testing import CliRunner

from farmer.cli import cli


@patch('signal.pause')
class CLITestCase(unittest.TestCase):
    def test_start_gives_error_if_broker_is_missing(self, pause_mock):
        runner = CliRunner()
        result = runner.invoke(cli, ['start'])
        self.assertTrue(result.exit_code > 0)
        self.assertIn('Missing option "--broker" / "-b"', result.output)

    @patch('farmer.application.Farmer.start')
    def test_starts_farmer(self, pause_mock, start_patch):
        runner = CliRunner()
        result = runner.invoke(cli, ['start', '--broker', 'redis://localhost'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(start_patch.call_count, 1)
