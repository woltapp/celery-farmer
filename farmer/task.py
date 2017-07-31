from __future__ import absolute_import

def get_tags(task):
    tags = {}
    return {
        "name": task.name,
        "worker": task.hostname,
    }
