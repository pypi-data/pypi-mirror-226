"""
Prometheus is an open source application monitoring system that offers a simple, text-based metrics
format to give you an efficient way to handle a large amount of metrics data.
With a powerful query language, you can visualize data and manage alerts.
Prometheus supports various integrations, including with Grafana for a visual dashboard or
 with PageDuty and Slack for alert notifications. Prometheus also supports numerous products,
  including database products, server applications, Kubernetes, and Java Virtual Machines.

Install promethus serer: prometheus-installation-on-windows:
http://www.liferaysavvy.com/2021/07/prometheus-installation-on-windows.html

Download the zip file: https://prometheus.io/download/
Downloads//prometheus//prometheus-2.36.2.windows-amd64/

Extract and open the prometheus.yml file and add the following
  - job_name: "fast_api_py_app"
    static_configs:
      - targets: ["localhost:8080"]

under:
scrape_configs:
  # The job name is added as a label job=<job_name> to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to /metrics
    # scheme defaults to http.

    static_configs:
      - targets: ["localhost:9090"]
  - job_name: "fast_api_py_app"
    static_configs:
      - targets: ["localhost:8080"]


Now run the exe file: double click
Downloads//prometheus//prometheus-2.36.2.windows-amd64//prometheus.exe

Now browse the prometheus server: http://localhost:9090/

Now start your fast api python app running on port 8080

and then search the metrics with name atlas_vm_backup_size_logical_bytes


Grifana integration:
Download the grafana installer: https://grafana.com/grafana/download?platform=windows
https://grafana.com/docs/grafana/latest/setup-grafana/installation/windows/

Install the grifana, once installed The default Grafana port is 3000
To run Grafana, open your browser and go to the Grafana port (http://localhost:3000/ is default) and then follow the instructions in Getting Started.

defaulr username/password is admin/admin, change the password
now: admin/Hpe@1234

Now add data source:
click in setting icon from left side: slecte data source-> add data source->Select prometheus-> Add url: http://localhost:9090
click save and test and then clcick on explore and search your metrics

"""

from prometheus_client import start_http_server, Histogram
import random
import time
from math import inf

buckets = [1, 2, 5, 10, inf]
vm_backup_size_bucket_bytes = (
    1000000000,  # (1 GB) 1e+09
    2000000000,  # (2 GB) 2e+09
    5000000000,  # (5 GB) 5e+09
    10000000000,  # (10 GB) 1e+010
    20000000000,  # (20 GB) 2e+010
    50000000000,  # (50 GB) 5e+010
    100000000000,  # (100 GB) 1e+011
    200000000000,  # (200 GB) 2e+011
    500000000000,  # (500 GB) 5e+011
    1000000000000,  # (1 TB)  1e+012
    2000000000000,  # (2 TB)  2e+012
    5000000000000,  # (5 TB)  5e+012
    10000000000000,  # (10 TB) 1e+013
    20000000000000,  # (20 TB) 2e+013
    50000000000000,  # (50 TB) 5e+013
    100000000000000,  # (100 TB) 1e+014
    200000000000000,  # (200 TB) 2e+014
    500000000000000,  # (500 TB) 5e+014
    1000000000000000,  # (1 PB)  1e+015
    inf
)
SOME_MEASURE= Histogram(
    'atlas_vm_backup_size_logical_bytes2',
    'VM Backup size',
    buckets=vm_backup_size_bucket_bytes,
    labelnames=["app_type", "backup_type"])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)

    backup_sizes = [
        1000000000,
        2000000000,
        3000000000,
        4000000000,
        5000000000,
        6000000000,
        7000000000,
        8000000000,
        9000000000,
        10000000000,
        11000000000,
        12000000000,
        13000000000
    ]
    d = {int(i/1000000000):0 for i in backup_sizes}
    i = 0
    backup_types = ['backup', 'cloud_backup', 'snapshots']
    while True:
        b = random.choice(backup_sizes)
        size_in_gb = int(b/1000000000)
        print(f'Backup Size : {size_in_gb} GB')
        if size_in_gb in d:
            d[size_in_gb] = d[size_in_gb] + 1
        print(d)
        backup_type = random.choice(range(0, 3))
        print(f'Backup type: {backup_types[backup_type]}')
        SOME_MEASURE.labels(app_type="vmware", backup_type=backup_types[backup_type]).observe(b)
        #SOME_MEASURE.collect()
        time.sleep(.2)
        if i == 500:
            print('sleeping....')
            time.sleep(20 * 60 * 60)
        i += 1

"""

Browse: http://localhost:8000/
or http://localhost:8000/metrics

Backup type: snapshots
Backup Size : 10 GB
{1: 47, 2: 40, 3: 37, 4: 39, 5: 49, 6: 45, 7: 38, 8: 33, 9: 34, 10: 29, 11: 40, 12: 41, 13: 27}
Backup type: cloud_backup
Backup Size : 5 GB
{1: 47, 2: 40, 3: 37, 4: 39, 5: 50, 6: 45, 7: 38, 8: 33, 9: 34, 10: 29, 11: 40, 12: 41, 13: 27}
Backup type: backup
Backup Size : 11 GB
{1: 47, 2: 40, 3: 37, 4: 39, 5: 50, 6: 45, 7: 38, 8: 33, 9: 34, 10: 29, 11: 41, 12: 41, 13: 27}
Backup type: snapshots
sleeping....

http://localhost:8080/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 356.0
python_gc_objects_collected_total{generation="1"} 7.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 47.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="5",version="3.6.5"} 1.0
# HELP atlas_vm_backup_size_logical_bytes2 VM Backup size
# TYPE atlas_vm_backup_size_logical_bytes2 histogram
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+09"} 16.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+09"} 28.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+09"} 70.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+010"} 126.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+010"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+010"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+011"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+011"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+011"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+012"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+012"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+012"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+013"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+013"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+013"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+014"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="2e+014"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="5e+014"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="1e+015"} 157.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="cloud_backup",le="+Inf"} 157.0
atlas_vm_backup_size_logical_bytes2_count{app_type="vmware",backup_type="cloud_backup"} 157.0
atlas_vm_backup_size_logical_bytes2_sum{app_type="vmware",backup_type="cloud_backup"} 1.016e+012
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+09"} 20.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+09"} 38.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+09"} 75.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+010"} 137.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+010"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+010"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+011"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+011"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+011"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+012"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+012"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+012"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+013"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+013"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+013"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+014"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="2e+014"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="5e+014"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="1e+015"} 175.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="backup",le="+Inf"} 175.0
atlas_vm_backup_size_logical_bytes2_count{app_type="vmware",backup_type="backup"} 175.0
atlas_vm_backup_size_logical_bytes2_sum{app_type="vmware",backup_type="backup"} 1.131e+012
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+09"} 11.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+09"} 21.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+09"} 68.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+010"} 129.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+010"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+010"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+011"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+011"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+011"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+012"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+012"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+012"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+013"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+013"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+013"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+014"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="2e+014"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="5e+014"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="1e+015"} 169.0
atlas_vm_backup_size_logical_bytes2_bucket{app_type="vmware",backup_type="snapshots",le="+Inf"} 169.0
atlas_vm_backup_size_logical_bytes2_count{app_type="vmware",backup_type="snapshots"} 169.0
atlas_vm_backup_size_logical_bytes2_sum{app_type="vmware",backup_type="snapshots"} 1.187e+012
# HELP atlas_vm_backup_size_logical_bytes2_created VM Backup size
# TYPE atlas_vm_backup_size_logical_bytes2_created gauge
atlas_vm_backup_size_logical_bytes2_created{app_type="vmware",backup_type="cloud_backup"} 1.656556453157568e+09
atlas_vm_backup_size_logical_bytes2_created{app_type="vmware",backup_type="backup"} 1.6565564535725188e+09
atlas_vm_backup_size_logical_bytes2_created{app_type="vmware",backup_type="snapshots"} 1.6565564543887157e+09



Grafana panel bar guage:
{
  "id": 14,
  "gridPos": {
    "h": 12,
    "w": 24,
    "x": 0,
    "y": 4
  },
  "type": "bargauge",
  "title": "VM Backup size",
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {},
        "indexByName": {},
        "renameByName": {
          "+Inf": "1 PB+",
          "1e+010": "10 GB",
          "1e+011": "100 GB",
          "1e+012": "1 TB",
          "1e+013": "10 TB",
          "1e+014": "100 TB",
          "1e+015": "1 PB",
          "1e+09": "1 GB",
          "2e+010": "20 GB",
          "2e+011": "200 GB",
          "2e+012": "2 TB",
          "2e+013": "20 TB",
          "2e+014": "200 TB",
          "2e+09": "2 GB",
          "5e+010": "50 GB",
          "5e+011": "500 GB",
          "5e+012": "5 TB",
          "5e+013": "50 TB",
          "5e+014": "500 TB",
          "5e+09": "5 GB",
          "Time": ""
        }
      }
    }
  ],
  "datasource": {
    "type": "prometheus",
    "uid": "NfAsP7qnk"
  },
  "pluginVersion": "9.0.0",
  "fieldConfig": {
    "defaults": {
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          }
        ]
      },
      "color": {
        "mode": "thresholds"
      }
    },
    "overrides": []
  },
  "options": {
    "reduceOptions": {
      "values": false,
      "calcs": [
        "lastNotNull"
      ],
      "fields": ""
    },
    "orientation": "auto",
    "displayMode": "gradient",
    "showUnfilled": true,
    "minVizWidth": 0,
    "minVizHeight": 10
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "uid_prometheus_grafana_datasource"
      },
      "editorMode": "code",
      "exemplar": true,
      "expr": "sum by (le) (atlas_vm_backup_size_logical_bytes2_bucket)",
      "format": "heatmap",
      "interval": "",
      "legendFormat": "{{le}}",
      "range": true,
      "refId": "A"
    }
  ],
  "transparent": true,
  "description": ""
}
"""