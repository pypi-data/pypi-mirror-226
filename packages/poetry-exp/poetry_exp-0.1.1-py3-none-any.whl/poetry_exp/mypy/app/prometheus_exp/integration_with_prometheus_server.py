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
SOME_MEASURE= Histogram(
    'atlas_vm_backup_size_logical_bytes',
    'VM Protection Groups total',
    buckets=buckets,
    labelnames=["app_type", "backup_type"])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(0.5)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(3)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(3)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(3)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(6)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(6)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(11)
    # SOME_MEASURE.labels(app_type="vmware", backup_type="backup").observe(11)


    backup_sizes = range(1,10)
    d = {i:0 for i in backup_sizes}
    i = 0
    backup_types = ['backup', 'cloud_backup', 'snapshots']
    while True:
        b = random.choice(range(1,10))
        print(f'Size : {b} GB')
        if b in d:
            d[b] = d[b] + 1
        print(d)
        backup_type = random.choice(range(0,2))
        print(f'Backup type: {backup_types[backup_type]}')
        SOME_MEASURE.labels(app_type="vmware", backup_type=backup_types[backup_type]).observe(b)
        SOME_MEASURE.collect()
        time.sleep(.2)
        if i == 10:
            print('sleeping....')
            time.sleep(20 * 60 * 60)
        i += 1

"""

Browse: http://localhost:8000/
or http://localhost:8000/metrics

Bucket: 4
{1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
Bucket: 6
{1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}
Bucket: 2
{1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0, 9: 0}
Bucket: 7
{1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 1, 8: 0, 9: 0}

Bucket: 1
{1: 4, 2: 8, 3: 5, 4: 9, 5: 4, 6: 3, 7: 5, 8: 8, 9: 4}
Bucket: 3
{1: 4, 2: 8, 3: 6, 4: 9, 5: 4, 6: 3, 7: 5, 8: 8, 9: 4}
sleeping....


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
python_gc_collections_total{generation="0"} 46.0
python_gc_collections_total{generation="1"} 4.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="6",patchlevel="5",version="3.6.5"} 1.0
# HELP atlas_vm_backup_size_logical_bytes VM Protection Groups total
# TYPE atlas_vm_backup_size_logical_bytes histogram
atlas_vm_backup_size_logical_bytes_bucket{app_type="vmware",assets_category="vmfs_vms",le="1.0"} 4.0
atlas_vm_backup_size_logical_bytes_bucket{app_type="vmware",assets_category="vmfs_vms",le="2.0"} 12.0    # 12-4 =8
atlas_vm_backup_size_logical_bytes_bucket{app_type="vmware",assets_category="vmfs_vms",le="5.0"} 31.0    #31=12 = 19
atlas_vm_backup_size_logical_bytes_bucket{app_type="vmware",assets_category="vmfs_vms",le="10.0"} 51.0   #51-31 = 20
atlas_vm_backup_size_logical_bytes_bucket{app_type="vmware",assets_category="vmfs_vms",le="+Inf"} 51.0   #51-51 = 0
atlas_vm_backup_size_logical_bytes_count{app_type="vmware",assets_category="vmfs_vms"} 51.0
atlas_vm_backup_size_logical_bytes_sum{app_type="vmware",assets_category="vmfs_vms"} 247.0
# HELP atlas_vm_backup_size_logical_bytes_created VM Protection Groups total
# TYPE atlas_vm_backup_size_logical_bytes_created gauge
atlas_vm_backup_size_logical_bytes_created{app_type="vmware",assets_category="vmfs_vms"} 1.6554429897823124e+09





Grifana guage:
{
  "id": 8,
  "gridPos": {
    "h": 12,
    "w": 24,
    "x": 0,
    "y": 29
  },
  "type": "gauge",
  "title": "Backup count by size (bytes)",
  "datasource": {
    "uid": "NfAsP7qnk",
    "type": "prometheus"
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
        "mode": "palette-classic"
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
    "showThresholdLabels": false,
    "showThresholdMarkers": true,
    "legend": {
      "calcs": [],
      "displayMode": "list",
      "placement": "bottom"
    },
    "tooltip": {
      "mode": "single",
      "sort": "none"
    }
  },
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "NfAsP7qnk"
      },
      "exemplar": true,
      "expr": "sum(atlas_vm_backup_size_logical_bytes_bucket) by (le)",
      "interval": "",
      "legendFormat": "{{le}}",
      "refId": "A",
      "editorMode": "code",
      "range": true,
      "format": "heatmap"
    }
  ],
  "transparent": true,
  "description": "",
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {},
        "indexByName": {},
        "renameByName": {
          "1.0": "1 GB",
          "2.0": "2 GB",
          "5.0": "5 GB",
          "10.0": "10 GB",
          "+Inf": "10 GB +"
        }
      }
    }
  ]
}







Heatmap:
{
  "id": 19,
  "gridPos": {
    "h": 13,
    "w": 24,
    "x": 0,
    "y": 4
  },
  "type": "heatmap",
  "title": "Total backups",
  "datasource": {
    "uid": "NfAsP7qnk",
    "type": "prometheus"
  },
  "pluginVersion": "9.0.0",
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "NfAsP7qnk"
      },
      "exemplar": false,
      "expr": "sum by (le) (increase(atlas_vm_backup_size_logical_bytes_bucket[$__interval]))",
      "interval": "",
      "legendFormat": "{{le}}",
      "refId": "A",
      "editorMode": "code",
      "range": true,
      "format": "heatmap",
      "instant": false
    }
  ],
  "transparent": true,
  "transformations": [],
  "description": "",
  "heatmap": {},
  "cards": {
    "cardPadding": null,
    "cardRound": null
  },
  "color": {
    "mode": "spectrum",
    "cardColor": "#b4ff00",
    "colorScale": "sqrt",
    "exponent": 0.5,
    "colorScheme": "interpolateOranges"
  },
  "legend": {
    "show": true
  },
  "dataFormat": "tsbuckets",
  "yBucketBound": "auto",
  "reverseYBuckets": false,
  "xAxis": {
    "show": true
  },
  "yAxis": {
    "show": true,
    "format": "decgbytes",
    "decimals": 0,
    "logBase": 1,
    "splitFactor": null,
    "min": null,
    "max": null
  },
  "xBucketSize": null,
  "xBucketNumber": null,
  "yBucketSize": null,
  "yBucketNumber": null,
  "tooltip": {
    "show": true,
    "showHistogram": false
  },
  "highlightCards": true,
  "hideZeroBuckets": false,
  "maxDataPoints": 20
}
"""