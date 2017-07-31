# Farmer

![Image of farmer](https://www.collinsdictionary.com/images/thumb/farmer_96736501_250.jpg)

Farmer will monitor how the Celery cluster is behaving.

## Requirements

Install requirements with pip:
```
pip install -r requirements.txt
```

## Tests

Run tests with pytest:
```
pytest
```

## Running

For development, run `cli` directly with:
```
python farmer/cli.py start --broker=<celery_broker_url>
```
