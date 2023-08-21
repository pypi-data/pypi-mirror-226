from prometheus_client import start_http_server, Gauge
import random
import time
from datetime import datetime
VM_CUST_TOTAL = Gauge(
    "customers_total3",
    "Number of customers in VM inventory static",
    labelnames=("hypervisor_manager",))


def add_vcenters():
    customer_counts = 1
    VM_CUST_TOTAL.labels(hypervisor_manager="vmware").set(customer_counts)
    print(f'No. of customers# {customer_counts}, time: {datetime.now()}')

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