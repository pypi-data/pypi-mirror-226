from prometheus_client import start_http_server, Histogram
import random
import time
from math import inf

SOME_MEASURE= Histogram(
    'atlas_vm_protection_groups_total',
    'VM Protection Groups total',
    buckets=(1, 2, 5, 10, inf),
    labelnames=("app_type",))


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    cust_pg_count = {
        1:0,
        2:0,
        3:0,
        4:0,
        5:0,
        6:0,
        7:0,
        8:0,
        9:0,
        10:0
    }
    cust_ids = range(1, 10)
    i = 0
    while True:
        cust_id = random.choice(cust_ids)
        print(f'cust_id: {cust_id}')
        pg_count = cust_pg_count.get(cust_id) + 1
        print(f'pg_count: {pg_count}')
        print(cust_pg_count)
        SOME_MEASURE.labels(app_type="vmware").observe(pg_count)
        cust_pg_count[cust_id] = pg_count
        time.sleep(0.1)
        i += 1
        if i == 50:
            time.sleep(10 * 60 *60)





"""
Browse: http://localhost:8000/
or http://localhost:8000/metrics

Bucket: inf
{1: 9, 2: 9, 5: 10, 10: 11}
Bucket: 5
{1: 9, 2: 9, 5: 11, 10: 11}
Bucket: 2
{1: 9, 2: 10, 5: 11, 10: 11}
Bucket: inf
.....


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
# HELP atlas_vm_backups_size VM Protection Groups total
# TYPE atlas_vm_backups_size histogram
atlas_vm_backups_size_bucket{app_type="vmware",assets_category="vmfs_vms",le="1.0"} 9.0
atlas_vm_backups_size_bucket{app_type="vmware",assets_category="vmfs_vms",le="2.0"} 19.0
atlas_vm_backups_size_bucket{app_type="vmware",assets_category="vmfs_vms",le="5.0"} 30.0
atlas_vm_backups_size_bucket{app_type="vmware",assets_category="vmfs_vms",le="10.0"} 41.0
atlas_vm_backups_size_bucket{app_type="vmware",assets_category="vmfs_vms",le="+Inf"} 53.0
atlas_vm_backups_size_count{app_type="vmware",assets_category="vmfs_vms"} 53.0
atlas_vm_backups_size_sum{app_type="vmware",assets_category="vmfs_vms"} +Inf
# HELP atlas_vm_backups_size_created VM Protection Groups total
# TYPE atlas_vm_backups_size_created gauge
atlas_vm_backups_size_created{app_type="vmware",assets_category="vmfs_vms"} 1.6550950753454208e+09
"""