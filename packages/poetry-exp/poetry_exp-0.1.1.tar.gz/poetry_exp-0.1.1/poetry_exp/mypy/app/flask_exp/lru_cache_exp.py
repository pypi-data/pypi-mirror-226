# will work in python 3
from functools import lru_cache
import time

# lru cahche maintains a dict where it stores the input as a key and value the result of methods
# based on size, it will remove the lease frequent used valuse from dict if overfills the size
@lru_cache(maxsize=16)  # changing the maxsize value will affect the computation time
def fib(n):
    if n==0 or n==1:
        return 1
    else:
        return fib(n-1) +fib(n-2)

t1 = time.time()
fib_nums = [fib(num) for num in range(35)]
t2 = time.time()
print(fib_nums)
print(t2-t1)