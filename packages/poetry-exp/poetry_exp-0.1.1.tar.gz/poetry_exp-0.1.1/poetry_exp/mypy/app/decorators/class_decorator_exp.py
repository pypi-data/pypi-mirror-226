from functools import wraps


class logit(object):
    def __init__(self, log_file='out.log'):
        self.log_file=log_file

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            log_string = '\nFunction {0} called with args: {1} and kwargs: {2}, result: {3}'.format(
                func.__name__, args, kwargs, result)
            print log_string
            with open(self.log_file, 'a') as f:
                f.write(log_string)
            self.notify()
            return result
        return wrapper

    def notify(self):
        # Send notification
        pass


@logit(log_file='test.log')
def add(a, b=10):
    return a+b


add(10)
add(10, b=40) #Function add called with args: (10,) and kwargs: {'b': 40}, result: 50
print add.__name__  # add


class logit_email(logit):
    def __init__(self, email='abc@yahoo.com', *args, **kwargs):
        self.email=email
        super(logit_email, self).__init__(*args, **kwargs)

    def notify(self):
        print 'sending email to ', self.email

@logit_email(log_file='test.log')
def mul(a, b=10):
    return a*b

mul(10)