import time
import requests


class CircuitBreaker:
    def __init__(self, max_failures=3, reset_timeout=10):
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'

    def __call__(self, func):
        print('Call only once')
        def wrapper(*args, **kwargs):
            print('Calling wrapper ')
            if self.state == 'open' and self._timeout_expired():
                print(f'setting failure count 0')
                self.state = 'half-open'
                self.failure_count = 0
                response = func(*args, **kwargs)
                self._update_state(response)
                return response
            elif self.state == 'open':
                raise Exception('Circuit is open, requests are blocked')
            else:
                try:
                    print('Cicuit is closed')
                    response = func(*args, **kwargs)
                    print(response.status_code)
                    self._update_state(response)
                    return response
                except Exception as e:
                    print(e)
                    self._handle_failure()
                    raise e
        return wrapper

    def _handle_failure(self):
        self.failure_count += 1
        print(f'Handling failures, failure_count: {self.failure_count}')
        if self.failure_count >= self.max_failures:
            self.state = 'open'
            print(f'Opening the circuit')
            self.last_failure_time = time.time()

    def _update_state(self, response):
        if self.state == 'half-open' and response.status_code == 200:
            self.state = 'closed'
        elif self.state == 'half-open':
            self._handle_failure()

    def _timeout_expired(self):
        return time.time() - self.last_failure_time >= self.reset_timeout


@CircuitBreaker()
def call_external_service():
    response = requests.get("http://localhost:5000/home")
    print(response)
    return response
    #print(response.text)


if __name__ == '__main__':
   for i in range(100):
      try:
          call_external_service()
      except Exception as e:
          print(e)
      time.sleep(1)


"""
First run the flask_app_server.py
then after some time stop the flask_app_server.py
You can notice, requests will be blocked (Circuit is open, requests are blocked)
then restart the flask_app_server.py, then you can notice, it start serving
"""