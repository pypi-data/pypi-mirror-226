from prometheus_client import start_http_server, Gauge
import random
import time

VM_CUST_TOTAL = Gauge(
    "atlas_vm_customers_total_static",
    "Number of customers in VM inventory static",
    labelnames=("hypervisor_manager",))

VC_CUST_TOTAL = Gauge(
    "atlas_vm_hypervisor_managers_total_static",
    "Number of registered hypervisor managers",
    labelnames=("hypervisor_manager", "version"))

def add_customers(customer_count):
    print(f"Total no. of customers# {customer_count}")
    VM_CUST_TOTAL.clear()
    hm_types = ("vmwware", "hyper-v")
    cust_type_count = {hm_type: 0 for hm_type in hm_types}
    for i in range(0, customer_count):
        hypervisor_mgr_type = hm_types[random.choice(range(0, 2))]
        #print(f"Adding customer of type: {hypervisor_mgr_type}")
        VM_CUST_TOTAL.labels(hypervisor_manager=hypervisor_mgr_type).inc()
        cust_type_count[hypervisor_mgr_type] += 1
    print(cust_type_count)


def add_customers2():
    VM_CUST_TOTAL.clear()
    customer_counts = (
        ("vmware", random.choice(range(5, 10))),
        ("hyper-v", random.choice(range(5, 10)))
    )
    print(customer_counts)
    for customer in customer_counts:
        VM_CUST_TOTAL.labels(hypervisor_manager=customer[0]).inc(customer[1])


def add_vcenters():
    VC_CUST_TOTAL.clear()  # so that it does not increment on previous reading, instead fresh count we will be giving

    hm_type_customers = dict()
    vc_counts = (
        ("cust1", "vmware", "6.5", random.choice(range(5, 10))),
        ("cust2", "hyper-v", "6.5", random.choice(range(5, 10))),
        ("cust2", "vmware", "6.5", random.choice(range(5, 10))),
        ("cust1", "vmware", "6.7", random.choice(range(5, 10))),
        ("cust1", "hyper-v", "6.7", random.choice(range(5, 10))),

    )
    print(vc_counts)
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
    for hm_type, customers in hm_type_customers.items():
        print(hm_type, len(customers))
        VM_CUST_TOTAL.labels(hypervisor_manager=hm_type).inc(len(customers))

if __name__ == '__main__':
    start_http_server(8080)
    while True:
        customer_count = random.choice(range(5, 10))
        #add_customers(customer_count)
        #add_customers2()
        add_vcenters()

        time.sleep(10)
