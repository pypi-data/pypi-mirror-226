from functools import wraps
import time

REACHABLE_IPS = [
    '10.10.10.1',
    '10.10.10.2',
    '10.10.10.3',
    '10.10.10.4',
]


class Retry:
    def __init__(self, retry=1, delay=1, retry_condition_value=None):
        """
        :param retry: max attempt
        :param delay: delay in seconds for retry
        :param retry_condition_value: stop retrying if function result matches this value,
        If not passed, always execute function retry times irrespective of its result
        """
        print("Initializing param")
        # Will execute no of times decorate in function, not on no of calls
        self.retry = retry
        self.delay = delay
        self.retry_condition_value = retry_condition_value

    def __call__(self, func):
        print("Calling  func")
        # Will execute no of times decorate in function, not on no of calls

        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Calling  wrapper")
            # Will execute on no of times function calls
            result = None
            retry = self.retry
            retry_condition_value = self.retry_condition_value
            delay = self.delay
            while retry > 0:
                result = func(*args, **kwargs)
                if retry_condition_value is not None:
                    if result == retry_condition_value:
                        return result

                retry -= 1
                time.sleep(delay)
            return result
        return wrapper


@Retry(retry=3, delay=1,retry_condition_value=True)
def connect(ip):
    print('Connecting to {0}'.format(ip))
    if ip in REACHABLE_IPS:
        return True
    return False


@Retry(retry=2, delay=1, retry_condition_value=True)
def disconnect(ip):
    print('Disconnecting {0}'.format(ip))
    if ip not in REACHABLE_IPS:
        return True
    return False


if __name__ == '__main__':

    print('Connect Result: {0}'.format(connect('10.10.10.1')))
    print('Connect Result: {0}'.format(connect('20.10.10.1')))

    print('Disconnect Result: {0}'.format(disconnect('10.10.10.1')))
    print('Disconnect Result: {0}'.format(disconnect('20.10.10.1')))


