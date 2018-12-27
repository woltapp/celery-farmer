from celery_farmer.broker import RedisBroker


def test_parses_full_uri() -> None:
    assert RedisBroker('redis://localhost:6379/1/') is not None


def test_parses_uri_without_database() -> None:
    assert RedisBroker('redis://localhost:6379//') is not None
