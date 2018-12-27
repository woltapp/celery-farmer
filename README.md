# Farmer

![Image of farmer](https://www.collinsdictionary.com/images/thumb/farmer_96736501_250.jpg)

Farmer will monitor how the Celery cluster is behaving.

## Usage

### Requirements
- Python, versions 3.6 and 3.7 are supported
- Pip or Pipenv

### Install
Install package with pipenv:

```
pipenv install .
```

### Run
Run farmer with shell command:
```
farmer
```

### Configuration

## Development

### Requirements
- Pipenv

Clone repository and install development requirements with:
```
pipenv install --dev
```

### Running tests
Run all tests, typecheck and linter with:
```
pipenv run all-tests
```

Run only typecheck with:
```
pipenv run typecheck
```

Run only tests with:
```
pipenv run test
```
Or invoke `pytest` directly:
```
pytest
```

Run only linter with:
```
pipenv run lint
```
Or invoke `flake` directly:
```
flake8
```
