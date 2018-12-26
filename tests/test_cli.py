from unittest.mock import patch

from click.testing import CliRunner
from pytest import fixture

from farmer.cli import cli


@fixture
def _runner():
    return CliRunner()


@patch('signal.pause')
def test_start_gives_error_if_broker_is_missing(pause_mock, _runner):
    result = _runner.invoke(cli, ['start'])
    assert result.exit_code > 0
    assert 'Missing option "--broker" / "-b"' in result.output


@patch('signal.pause')
@patch('farmer.application.Farmer.start')
def test_starts_farmer(pause_mock, start_patch, _runner):
    result = _runner.invoke(cli, ['start', '--broker', 'redis://localhost'])
    assert result.exit_code == 0
    assert start_patch.call_count == 1
