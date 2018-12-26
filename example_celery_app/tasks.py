from celery import Celery

import time


app = Celery("tasks", broker="redis://localhost:6379/1")


@app.task
def add(x, y):
    print(f'Calculating sum of {x} and {y}')
    time.sleep(1)
    print("Calculated")
    return x + y
