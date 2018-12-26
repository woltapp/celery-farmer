from typing import Dict

from celery.events.state import State


def get_tags(task: State.Task) -> Dict[str, str]:
    return {
        'name': task.name,
        'worker': task.hostname,
    }
