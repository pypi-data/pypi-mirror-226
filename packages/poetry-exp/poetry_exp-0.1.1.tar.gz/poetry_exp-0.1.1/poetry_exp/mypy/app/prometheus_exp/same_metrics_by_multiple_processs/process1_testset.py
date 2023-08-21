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
        ("cust1", "vmware", "6.5", 4),
        ("cust2", "vmware", "6.5", 2),
        ("cust2", "vmware", "6.5", 1),
        ("cust1", "vmware", "6.7", 5),
        ("cust1", "vmware", "6.7", 5),

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

    # print(hm_type_customers)
    # customer_counts = 0
    # VM_CUST_TOTAL.clear()
    #
    # for hm_type, customers in hm_type_customers.items():
    #     print(hm_type, len(customers))
    #     customer_counts += len(customers)
    #     VM_CUST_TOTAL.labels(hypervisor_manager=hm_type).inc(len(customers))
    #print(f'No. of customers# {customer_counts}')

if __name__ == '__main__':
    start_http_server(8081)
    while True:
        customer_count = random.choice(range(5, 10))
        add_vcenters()
        time.sleep(5)


"""
configure multiple targets in prometeus.yaml
# my global config
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
  - job_name: "fast_api_py_app"
    static_configs:
      - targets: ["localhost:8080", "localhost:8081", "localhost:8082"]    



When you will run all three process, you can see the same metrics:
customers_total2{hypervisor_manager="vmware", instance="localhost:8081", job="fast_api_py_app"} 2
customers_total2{hypervisor_manager="vmware", instance="localhost:8082", job="fast_api_py_app"} 2
customers_total2{hypervisor_manager="vmware", instance="localhost:8083", job="fast_api_py_app"} 2

so it will show total 6, but we are intersted to show only 2

"""