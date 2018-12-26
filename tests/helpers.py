import time
from typing import Callable


def wait_until_success(function: Callable[[], None], poll_time: float = 0.1,
                       poll_count: int = 10) -> None:
    success = False
    for current_count in range(0, poll_count):
        try:
            function()
            success = True
            break
        except Exception:
            time.sleep(poll_time)

    if not success:
        assert False, f'Waited {poll_time * poll_count}s without success'
