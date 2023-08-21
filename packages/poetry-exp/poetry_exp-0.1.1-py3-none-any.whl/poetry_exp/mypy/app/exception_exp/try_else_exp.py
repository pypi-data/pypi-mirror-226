"""
When we want some code to run if no exception occurs,
The else clause would only run if no exception occurs and it would run before the
finally clause

"""

try:
    print 'Excuted'
except Exception:
    print 'Exception occurred'
else:
   print 'No exception occurred'
finally:
    print "This would be printed in every case"

"""
Excuted
No exception occurred
This would be printed in every case

"""

try:
    a = 4/0
except Exception:
    print 'Exception occurred'
else:
   print 'No exception occurred '
finally:
    print "This would be printed in every case"


""" Exception occurred
This would be printed in every case
"""