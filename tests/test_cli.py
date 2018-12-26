from unittest.mock import patch

from click.testing import CliRunner

from farmer.cli import cli


@patch('signal.pause')
def test_start_gives_error_if_broker_is_missing(pause_mock):
    runner = CliRunner()
    result = runner.invoke(cli, ['start'])
    assert result.exit_code > 0
    assert 'Missing option "--broker" / "-b"' in result.output


@patch('signal.pause')
@patch('farmer.application.Farmer.start')
def test_starts_farmer(pause_mock, start_patch):
    runner = CliRunner()
    result = runner.invoke(cli, ['start', '--broker', 'redis://localhost'])
    assert result.exit_code == 0
    assert start_patch.call_count == 1
