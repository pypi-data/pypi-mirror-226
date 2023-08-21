from prometheus_client import start_http_server, Histogram
import random
import time
from math import inf

buckets = [1, 2, 5, 10, inf]
SOME_MEASURE= Histogram(
    'atlas_vm_protection_groups_total',
    'VM Protection Groups total',
    buckets=buckets,
    labelnames=["app_type", "assets_category"])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        for i in range(20):
            if i%2 == 0:
               with SOME_MEASURE.labels(app_type="vmware", assets_category="vmfs_vms").time():
                   time.sleep(1)
            else:
               with SOME_MEASURE.labels(app_type="vmware", assets_category="vvol_vms").time():
                   time.sleep(5)
        # time.sleep(5)


"""
Browse: http://localhost:8000/
or http://localhost:8000/metrics

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
# HELP atlas_vm_protection_groups_total VM Protection Groups total
# TYPE atlas_vm_protection_groups_total histogram
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vmfs_vms",le="1.0"} 1.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vmfs_vms",le="2.0"} 82.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vmfs_vms",le="5.0"} 82.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vmfs_vms",le="10.0"} 82.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vmfs_vms",le="+Inf"} 82.0
atlas_vm_protection_groups_total_count{app_type="vmware",assets_category="vmfs_vms"} 82.0
atlas_vm_protection_groups_total_sum{app_type="vmware",assets_category="vmfs_vms"} 82.42160318952574
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vvol_vms",le="1.0"} 0.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vvol_vms",le="2.0"} 0.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vvol_vms",le="5.0"} 2.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vvol_vms",le="10.0"} 81.0
atlas_vm_protection_groups_total_bucket{app_type="vmware",assets_category="vvol_vms",le="+Inf"} 81.0
atlas_vm_protection_groups_total_count{app_type="vmware",assets_category="vvol_vms"} 81.0
atlas_vm_protection_groups_total_sum{app_type="vmware",assets_category="vvol_vms"} 405.44243517942533
# HELP atlas_vm_protection_groups_total_created VM Protection Groups total
# TYPE atlas_vm_protection_groups_total_created gauge
atlas_vm_protection_groups_total_created{app_type="vmware",assets_category="vmfs_vms"} 1.6547728479597187e+09
atlas_vm_protection_groups_total_created{app_type="vmware",assets_category="vvol_vms"} 1.6547728489694476e+09
"""