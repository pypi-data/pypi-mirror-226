
class InvalidUserException(Exception):

    def __init__(self, username, error_code):
        super(InvalidUserException, self).__init__("Invalid user {0}".format(username))
        self.error_code = error_code

        # OR
        #Exception.__init__(self, "Invalid user {0}".format(username))



if __name__ == '__main__':
    try:
        #i = 2/0  # will not caught ZeroDivisionError
        d = {}
        #print d['a']  # will not be caught KeyError: 'a'

        user = None
        if user is None:
            raise InvalidUserException(user, 404)
    except InvalidUserException as e:
        print 'Caught exception, error:', e.message, " error code: ", e.error_code

