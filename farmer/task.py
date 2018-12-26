
def get_tags(task):
    return {
        'name': task.name,
        'worker': task.hostname,
    }
