"""
Under the hood, it works by temporarily swapping out the “normal” versions of the libraries in sys.modules for an eventlet.green equivalent. When the import of the to-be-patched module completes, the state of sys.modules is restored. Therefore, if the patched module contains the statement ‘import socket’, import_patched will have it reference eventlet.green.socket. One weakness of this approach is that it doesn’t work for late binding (i.e. imports that happen during runtime). Late binding of imports is fortunately rarely done (it’s slow and against PEP-8), so in most cases import_patched will work just fine.


"""



import threading
print threading.current_thread.__module__
#threading
import eventlet
print threading.current_thread.__module__
#threading
eventlet.monkey_patch() #swap out the standard lib module by eventlet.green
print threading.current_thread.__module__
#eventlet.green.threading
 
#Selectively, we can do
eventlet.monkey_patch(socket=True, select=True)
