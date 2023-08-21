from prometheus_client import start_http_server, Gauge
import random
import time

VM_CUST_TOTAL = Gauge(
    "test_drop",
    "Number of customers in VM inventory",
    labelnames=("hypervisor_manager_type",))


def add_customer(hypervisor_manager_type):
    print(f"Adding customer of type: {hypervisor_mgr_type}")
    VM_CUST_TOTAL.labels(hypervisor_manager_type=hypervisor_manager_type).inc()


def delete_customer(hypervisor_manager_type):
    print(f"Deleting customer of type: {hypervisor_mgr_type}")
    VM_CUST_TOTAL.labels(hypervisor_manager_type=hypervisor_manager_type).dec()


if __name__ == '__main__':
    start_http_server(8081)
    hm_types = ("vmwware", "hyper-v")
    while True:
        choice = random.choice(range(1, 10))
        #print(type(choice))
        hypervisor_mgr_type = hm_types[random.choice(range(0,2))]
        print(hypervisor_mgr_type)
        add_customer(hypervisor_mgr_type)

        if choice % 2 == 0:
            delete_customer(hypervisor_mgr_type)

        time.sleep(3)
