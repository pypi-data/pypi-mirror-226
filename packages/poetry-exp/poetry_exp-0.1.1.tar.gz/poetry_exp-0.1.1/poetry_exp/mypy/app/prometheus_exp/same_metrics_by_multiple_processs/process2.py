from prometheus_client import start_http_server, Gauge
import random
import time

VM_CUST_TOTAL = Gauge(
    "customers_total2",
    "Number of customers in VM inventory static",
    labelnames=("hypervisor_manager",))

VC_CUST_TOTAL = Gauge(
    "hypervisor_managers_total",
    "Number of registered hypervisor managers",
    labelnames=("hypervisor_manager", "version"))


def add_vcenters():
    # VC_CUST_TOTAL.clear()  # so that it does not increment on previous reading, instead fresh count we will be giving

    hm_type_customers = dict()
    vc_counts = (
        ("cust1", "vmware", "6.5", random.choice(range(5, 10))),
        ("cust2", "vmware", "6.5", random.choice(range(5, 10))),
        ("cust2", "vmware", "6.5", random.choice(range(5, 10))),
        ("cust1", "vmware", "6.7", random.choice(range(5, 10))),
        ("cust1", "vmware", "6.7", random.choice(range(5, 10))),

    )
    print(vc_counts)
    VC_CUST_TOTAL.clear()
    for vc in vc_counts:
        hm_type = vc[1]
        cust_id = vc[0]
        if hm_type in hm_type_customers:
            hm_type_customers[hm_type].add(cust_id)
        else:
            s = set()
            s.add(cust_id)
            hm_type_customers[hm_type] = s

        VC_CUST_TOTAL.labels(hypervisor_manager=hm_type, version=vc[2]).inc(vc[3])

    print(hm_type_customers)
    customer_counts = 0
    VM_CUST_TOTAL.clear()
    for hm_type, customers in hm_type_customers.items():
        print(hm_type, len(customers))
        customer_counts += len(customers)
        VM_CUST_TOTAL.labels(hypervisor_manager=hm_type).inc(len(customers))
    print(f'No. of customers# {customer_counts}')

if __name__ == '__main__':
    start_http_server(8082)
    while True:
        customer_count = random.choice(range(5, 10))
        add_vcenters()
        time.sleep(1)
