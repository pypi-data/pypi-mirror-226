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


def add_vcenters():
    with open('cust_count') as f:
        customer_counts = f.readline()
        VM_CUST_TOTAL.labels(hypervisor_manager="vmware").set(customer_counts)
        print(f'No. of customers# {customer_counts}, time: {datetime.now()}')
        VM_CUST_TOTAL.collect()


if __name__ == '__main__':
    start_http_server(8083)
    while True:
        customer_count = random.choice(range(5, 10))
        add_vcenters()
        time.sleep(10)
