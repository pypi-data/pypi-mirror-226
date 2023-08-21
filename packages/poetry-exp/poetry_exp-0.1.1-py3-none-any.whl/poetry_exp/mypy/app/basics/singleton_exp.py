"""
There are situations where you need to create only one instance of data throughout the lifetime of a program.
 This can be a class instance, a list, or a dictionary, for example.
The creation of a second instance is undesirable. This can result in logical errors or malfunctioning of the program.
 The design pattern that allows you to create only one instance of data is called singleton.


Singleton is the best candidate when the requirements are as follows:

Controlling concurrent access to a shared resource
If you need a global point of access for the resource from multiple or different parts of the system
When you need to have only one object
Some typical use cases of using a singleton are:

The logging class and its subclasses (global point of access for the logging class to send messages to the log)
Printer spooler (your application should only have a single instance of the spooler in order to avoid having a conflicting request for the same resource)
Managing a connection to a database
File manager
Retrieving and storing information on external configuration files
Read-only singletons storing some global states (user language, time, time zone, application path, and so on)


All modules are singletons by nature because of Pythons module importing steps:

Check whether a module is already imported. If yes, return it. If not, find a module, initialize it, and return it.
Initializing a module means executing a code, including all module-level assignments.
When you import the module for the first time, all of the initializations will be done;
 however, if you try to import the module for the second time, Python will return the initialized module.
 Thus, the initialization will not be done, and you get a previously imported module with all of its data.

 https://hub.packtpub.com/python-design-patterns-depth-singleton-pattern/
"""


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print 'Creating object...'  # Execute only once
            cls.instance = super(Singleton, cls).__new__(cls)

        return cls.instance


class Logging(object):
    file = None

    def __init__(self, filename=None, log_level=None):
        print 'comes here2...........'
        self.filename = filename
        self.log_level = log_level

    def __new__(cls, *args, **kwargs):
        print 'comes here....1'
        if not hasattr(cls, 'instance'):
            print 'creating Log object'
            cls.instance = super(Logging, cls).__new__(cls)
            if kwargs.get('filename'):
               file = open(kwargs.get('filename'), 'a')
               print 'initializing file....', file
        return cls.instance


if __name__== '__main__':
    s1 = Singleton()
    s2 = Singleton()

    print s1
    print s2
    print s1 is s2 # True

    l1 = Logging(filename='test.log', log_level='Error')
    print l1
    print l1.log_level  # Error
    l2 = Logging(log_level='Info')
    print l2
    print l2.log_level  # Info
    print l1.log_level  # Info, Because same object
    print l1 is l2  # True

"""
    Creating object...
<__main__.Singleton object at 0x0000000002E30E10>
<__main__.Singleton object at 0x0000000002E30E10>
True
creating Log object
<open file 'test.log', mode 'a' at 0x0000000002FEC270>
<__main__.Logging object at 0x00000000030922E8>
<__main__.Logging object at 0x00000000030922E8>
True
"""