from typing import Any, Dict

task_received: Dict[str, Any] = {
    'retries': 0,
    'expires': None,
    'name': 'tasks.add',
    'clock': 8089,
    'timestamp': 1501507843.900996,
    'args': '(1, 2)',
    'pid': 24317,
    'utcoffset': -3,
    'eta': None,
    'local_received': 1501507843.901737,
    'kwargs': '{}',
    'type': 'task-received',
    'hostname': 'celery@Valtteris-MacBook-Pro-2.local',
    'uuid': '58369920-91ae-4825-9f22-72cf1dbd66b6'
}

task_started: Dict[str, Any] = {
    'local_received': 1501507843.903568,
    'uuid': '58369920-91ae-4825-9f22-72cf1dbd66b6',
    'clock': 8090,
    'timestamp': 1501507843.90302,
    'hostname': 'celery@Valtteris-MacBook-Pro-2.local',
    'pid': 24317,
    'utcoffset': -3,
    'type': 'task-started'
}

task_succeeded: Dict[str, Any] = {
    'local_received': 1501507843.904243,
    'uuid': '58369920-91ae-4825-9f22-72cf1dbd66b6',
    'clock': 8091,
    'timestamp': 1501507843.90374,
    'hostname': 'celery@Valtteris-MacBook-Pro-2.local',
    'pid': 24317,
    'utcoffset': -3,
    'result': "'3'",
    'runtime': 0.0014360779896378517,
    'type': 'task-succeeded'
}

active_queues_response: Dict[str, Any] = {
    'celery@foobar': [{
        'exclusive': False,
        'name': 'celery',
        'exchange': {
            'name': 'celery',
            'durable': True,
            'delivery_mode': 2,
            'passive': False,
            'arguments': None,
            'type': 'direct',
            'auto_delete': False
        },
        'durable': True,
        'routing_key': 'celery',
        'no_ack': False,
        'alias': None,
        'queue_arguments': None,
        'binding_arguments': None,
        'bindings': [],
        'auto_delete': False
    }, {
        'exclusive': False,
        'name': 'foobar',
        'exchange': {
            'name': 'foobar',
            'durable': True,
            'delivery_mode': 2,
            'passive': False,
            'arguments': None,
            'type': 'direct',
            'auto_delete': False
        },
        'durable': True,
        'routing_key': 'foobar',
        'no_ack': False,
        'alias': None,
        'queue_arguments': None,
        'binding_arguments': None,
        'bindings': [],
        'auto_delete': False
    }, {
        'exclusive': False,
        'name': 'baz',
        'exchange': {
            'name': 'baz',
            'durable': True,
            'delivery_mode': 2,
            'passive': False,
            'arguments': None,
            'type': 'direct',
            'auto_delete': False
        },
        'durable': True,
        'routing_key': 'baz',
        'no_ack': False,
        'alias': None,
        'queue_arguments': None,
        'binding_arguments': None,
        'bindings': [],
        'auto_delete': False
    }],
    'celery@Valtteris-MacBook-Pro-2.local': [{
        'exclusive': False,
        'name': 'celery',
        'exchange': {
            'name': 'celery',
            'durable': True,
            'delivery_mode': 2,
            'passive': False,
            'arguments': None,
            'type': 'direct',
            'auto_delete': False
        },
        'durable': True,
        'routing_key': 'celery',
        'no_ack': False,
        'alias': None,
        'queue_arguments': None,
        'binding_arguments': None,
        'bindings': [],
        'auto_delete': False
    }, {
        'exclusive': False,
        'name': 'foobar',
        'exchange': {
            'name': 'foobar',
            'durable': True,
            'delivery_mode': 2,
            'passive': False,
            'arguments': None,
            'type': 'direct',
            'auto_delete': False
        },
        'durable': True,
        'routing_key': 'foobar',
        'no_ack': False,
        'alias': None,
        'queue_arguments': None,
        'binding_arguments': None,
        'bindings': [],
        'auto_delete': False
    }]
}
