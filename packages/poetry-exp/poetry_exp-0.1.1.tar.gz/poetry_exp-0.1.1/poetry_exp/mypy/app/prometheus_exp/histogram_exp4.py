from prometheus_client import start_http_server, Histogram
import random
import time
from math import inf

buckets = [1, 2, 5, 10, inf]
SOME_MEASURE= Histogram(
    'atlas_vm_backup_size_logical_bytes',
    'VM Protection Groups total',
    buckets=buckets,
    labelnames=["app_type", "assets_category"])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8080)
    backup_sizes = range(1,10)
    d = {i:0 for i in backup_sizes}
    i = 0
    while True:
        b = random.choice(range(1,10))
        print(f'Bucket: {b}')
        if b in d:
            d[b] = d[b] + 1
        print(d)
        SOME_MEASURE.labels(app_type="vmware", assets_category="vmfs_vms").observe(b)
        time.sleep(.2)
        if i == 50:
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
"""