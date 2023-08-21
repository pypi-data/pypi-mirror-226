"""
Python doesnt allow multi-threading in the truest sense of the word. It has a multi-threading package but
 if you want to multi-thread to speed your code up, then its usually not a good idea to use it.
Python has a construct called the Global Interpreter Lock (GIL).
The GIL makes sure that only one of your threads can execute at any one time.
 A thread acquires the GIL, does a little work, then passes the GIL onto the next thread.
  This happens very quickly so to the human eye it may seem like your threads are executing in parallel,
   but they are really just taking turns using the same CPU core.
   All this GIL passing adds overhead to execution. This means that if you want to make your code run faster
    then using the threading package often isnt a good idea.

There are reasons to use Pythons threading package. If you want to run some things simultaneously,
 and efficiency is not a concern, then its totally fine and convenient. Or if you are running code that
  needs to wait for something (like some IO) then it could make a lot of sense.
   But the threading library wont let you use extra CPU cores.

Multi-threading can be outsourced to the operating system (by doing multi-processing),
 some external application that calls your Python code (eg, Spark or Hadoop),
  or some code that your Python code calls (eg: you could have your Python code
   call a C function that does the expensive multi-threaded stuff).
"""