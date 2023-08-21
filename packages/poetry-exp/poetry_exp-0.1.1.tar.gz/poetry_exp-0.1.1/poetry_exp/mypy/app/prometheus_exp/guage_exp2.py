from prometheus_client import start_http_server, Gauge
import random
import time

VM_CUST_TOTAL = Gauge(
    "test_atlas_vm_customers_total3",
    "Number of customers in VM inventory",
    labelnames=("hypervisor_manager", "customer_id"))


def add_customer(hypervisor_manager_type, customer_id):
    print(f"Adding customer of type: {hypervisor_mgr_type}")
    VM_CUST_TOTAL.labels(hypervisor_manager=hypervisor_manager_type, customer_id=customer_id).inc()


def delete_customer(hypervisor_manager_type, customer_id):
    print(f"Deleting customer of type: {hypervisor_mgr_type}")
    VM_CUST_TOTAL.labels(hypervisor_manager=hypervisor_manager_type, customer_id=customer_id).dec()


if __name__ == '__main__':
    start_http_server(8080)
    hm_types = ("vmware", "hyper-v")
    while True:
        choice = random.choice(range(1, 5))
        #print(type(choice))
        hypervisor_mgr_type = hm_types[random.choice(range(0,2))]
        print(hypervisor_mgr_type)
        add_customer(hypervisor_mgr_type, choice)

        if choice % 2 == 0:
            delete_customer(hypervisor_mgr_type, choice)

        time.sleep(2)
