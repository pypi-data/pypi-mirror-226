from prometheus_client import start_http_server, Gauge
import random
import time
from datetime import datetime

VM_CUST_TOTAL = Gauge(
    "customers_total3",
    "Number of customers in VM inventory static",
    labelnames=("hypervisor_manager",))

VC_CUST_TOTAL = Gauge(
    "hypervisor_managers_total",
    "Number of registered hypervisor managers",
    labelnames=("hypervisor_manager", "version"))

cust_count = 0
def add_vcenters():
    global cust_count

    VM_CUST_TOTAL.labels(hypervisor_manager="vmware").inc()
    cust_count += 1
    print(f'No. of customers# {cust_count}, time: {datetime.now()}')

if __name__ == '__main__':
    start_http_server(8083)
    while True:
        customer_count = random.choice(range(5, 10))
        add_vcenters()
        time.sleep(10)
