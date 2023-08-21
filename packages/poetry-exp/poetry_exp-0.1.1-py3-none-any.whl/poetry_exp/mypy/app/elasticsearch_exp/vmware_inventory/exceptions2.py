# (C) Copyright 2020 Hewlett Packard Enterprise Development Company, L.P.
# from oslo_log import log
#
# LOG = log.getLogger(__name__)
#


class VMWareBaseException(Exception):
    def __init__(self, message, *msg_args):
        self.message = message.format(*msg_args)
        super(VMWareBaseException, self).__init__(self.message)


class ResourceNotFound(VMWareBaseException):
    def __init__(self, *msg_args):
        self.message = "Resource '{0}' not found."
        super(VMNotFound, self).__init__(self.message, *msg_args)


class VMNotFound(VMWareBaseException):
    def __init__(self, *msg_args, **debug_args):
        self.message = "Virtual Machine '{0}' not found in vCenter '{1}'."
        super(VMNotFound, self).__init__(self.message, *msg_args, **debug_args)


def log_exception(exc_obj, debug_args):
    print('An exception occurred, Error: {0}'.format(str(exc_obj)))
    #LOG.exception('An exception occurred, Error: {0}'.format(str(exc_obj)))
    if debug_args:
        for k, v in exc_obj.debug_args.items():
            print('[Debug args] {0}: {1} '.format(k, v))
            #LOG.info('[Debug args] {0}: {1} '.format(k, v))


def raise_exception(exc_obj):
    log_exception(exc_obj)
    raise exc_obj


def test_known_exception():
    debug_args = []
    try:

        raise VMNotFound('vm1', 'vcnter1', type='vm', moref='vm-1', inventory_response={"vms": [], "ds": []})
    except Exception as e:
        raise_exception(e)


def test_unknown_exception():
    debug_args = {}
    try:
        debug_args['name'] = 'vm1'
        raise Exception("Not a listed exception")
    except Exception as e:
        log_exception()


if __name__ == '__main__':
    test_known_exception()
    test_unknown_exception()


