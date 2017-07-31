import time


def wait_until_success(function, poll_time=0.1, poll_count=10):
    success = False
    for current_count in range(0, poll_count):
        try:
            function()
            success = True
            break
        except:
            time.sleep(poll_time)

    if not success:
        raise AssertionError("Waited %ss without success" % str(poll_time * poll_count))
