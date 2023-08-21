from prometheus_client import start_http_server, Gauge
import random
import time

hm_register_failure_alert = Gauge(
    "hm_register_failure_alert",
    "Hypervisor manager register failure alert",
    labelnames=("hypervisor_manager", "customer_id"))


def add_customer(hypervisor_manager_type, customer_id):
    print(f"Adding customer of type: {hypervisor_mgr_type}")
    if customer_id % 2 == 0:
        hm_register_failure_alert.labels(hypervisor_manager=hypervisor_manager_type, customer_id=customer_id).set(1)


def delete_customer(hypervisor_manager_type, customer_id):
    print(f"Deleting customer of type: {hypervisor_mgr_type}")
    hm_register_failure_alert.labels(hypervisor_manager=hypervisor_manager_type, customer_id=customer_id).dec()


if __name__ == '__main__':
    start_http_server(8080)
    hm_types = ("vmware", "hyper-v")
    while True:
        choice = random.choice(range(1, 5))
        #print(type(choice))
        hypervisor_mgr_type = hm_types[random.choice(range(0,2))]
        print(hypervisor_mgr_type)
        add_customer(hypervisor_mgr_type, choice)

        # if choice % 2 == 0:
        #     delete_customer(hypervisor_mgr_type, choice)

        time.sleep(2)


"""
C:\\Users\\aafakmoh\\Downloads\\prometheus\\prometheus-2.36.2.windows-amd64>promtool check rules alert.rules.yml
Checking alert.rules.yml
  FAILED:
alert.rules.yml: yaml: unmarshal errors:
  line 13: cannot unmarshal !!map into string
C:\\Users\\aafakmoh\\Downloads\\prometheus\\prometheus-2.36.2.windows-amd64>

C:\\Users\\aafakmoh\\Downloads\\prometheus\\prometheus-2.36.2.windows-amd64>promtool check rules alert.rules.yml
Checking alert.rules.yml
  SUCCESS: 1 rules found


C:\\Users\\aafakmoh\\Downloads\\prometheus\\prometheus-2.36.2.windows-amd64>

http://localhost:9090/alerts?search=


# https://www.robustperception.io/sending-email-with-the-alertmanager-via-gmail/

C:\\Users\\aafakmoh\\Downloads\\prometheus-alertmanager\\alertmanager-0.25.0.windows-amd64>amtool.exe check-config alertmanager.yml
Checking 'alertmanager.yml'  SUCCESS
Found:
 - global config
 - route
 - 1 inhibit rules
 - 2 receivers
 - 0 templates


C:\\Users\\aafakmoh\\Downloads\\prometheus-alertmanager\\alertmanager-0.25.0.windows-amd64>

Download alertmanager:
  https://prometheus.io/download/#alertmanage
  
MOdify prometeous.yml:
# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093

restart prometheus server  and then browse alert manager UI:            
http://localhost:9093/#/alerts


EMail alert:
[FIRING:1] vmware_vcentre_reg_failure (hyper-v localhost:8080 fast_api_py_app glbr-vmware-protection critical cloud)
2 alerts for alertname=vmware_vcentre_reg_failure 

[1] Firing 
Labels
alertname = vmware_vcentre_reg_failure
customer_id = 4
hypervisor_manager = hyper-v
instance = localhost:8080
job = fast_api_py_app
owner = glbr-vmware-protection
severity = critical
source = cloud
Annotations
description = vCenter register failure alert
summary = vCenter register failed
Source


slack alert:
[FIRING:2] vmware_vcentre_reg_failure for fast_api_py_app (hypervisor_manager="hyper-v", instance="localhost:8080", job="fast_api_py_app", owner="glbr-vmware-protection", severity="critical", source="cloud")
Alert: vCenter register failed - critical Description: vCenter register failure alert Details:
  • alertname: vmware_vcentre_reg_failure
  • customer_id: 2
  • hypervisor_manager: hyper-v
  • instance: localhost:8080
  • job: fast_api_py_app
  • owner: glbr-vmware-protection
  • severity: critical
  • source: cloud
 
Alert: vCenter register failed - critical Description: vCenter register failure alert Details:
  • alertname: vmware_vcentre_reg_failure
  • customer_id: 4
  • hypervisor_manager: hyper-v
  • instance: localhost:8080
  • job: fast_api_py_app
  • owner: glbr-vmware-protection
  • severity: critical
  • source: cloud
"""


