from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/1")


@app.task
def add(x, y):
    print("Calculating sum of %i and %i" % (x, y))
    return x + y
