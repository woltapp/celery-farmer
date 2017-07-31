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

The farmer is intended to use in daemon mode in production, therefore currently the python process won't respect ctrl-c (Hopefully it will in the future). So to kill the running python process, figure out the PID and kill it with -9 directly.

One way to obtain the PID and kill would be:
```
ps aux | grep farmer.*start
<find correct process>
kill -9 <pid>
```
