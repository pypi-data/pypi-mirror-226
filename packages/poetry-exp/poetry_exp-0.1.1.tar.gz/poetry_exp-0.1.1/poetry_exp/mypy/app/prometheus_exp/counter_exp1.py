from prometheus_client import start_http_server, Counter
import random
import time
from math import inf

SOME_MEASURE= Counter(
    'atlas_vm_backup_count',
    'VM Protection Groups total',
    labelnames=["app_type", 'vm'])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    vm_ids = range(10)
    d = {"vm-"+str(i):0 for i in vm_ids}
    i = 0
    while True:
        vm_id = random.choice(vm_ids)
        vm_name = 'vm-' + str(vm_id)
        print(f'VM: {vm_name}')
        if vm_name in d:
            d[vm_name] = d[vm_name] + 1
        print(d)
        SOME_MEASURE.labels(app_type="vmware", vm=vm_name).inc()
        time.sleep(2)




"""
Browse: http://localhost:8000/
or http://localhost:8000/metrics

VM: vm-2
{'vm-0': 0, 'vm-1': 0, 'vm-2': 1, 'vm-3': 0, 'vm-4': 0, 'vm-5': 0, 'vm-6': 0, 'vm-7': 0, 'vm-8': 0, 'vm-9': 0}
VM: vm-9
{'vm-0': 0, 'vm-1': 0, 'vm-2': 1, 'vm-3': 0, 'vm-4': 0, 'vm-5': 0, 'vm-6': 0, 'vm-7': 0, 'vm-8': 0, 'vm-9': 1}
VM: vm-2
{'vm-0': 0, 'vm-1': 0, 'vm-2': 2, 'vm-3': 0, 'vm-4': 0, 'vm-5': 0, 'vm-6': 0, 'vm-7': 0, 'vm-8': 0, 'vm-9': 1}
VM: vm-2
{'vm-0': 0, 'vm-1': 0, 'vm-2': 3, 'vm-3': 0, 'vm-4': 0, 'vm-5': 0, 'vm-6': 0, 'vm-7': 0, 'vm-8': 0, 'vm-9': 1}
VM: vm-9

.....
VM: vm-4
{'vm-0': 1, 'vm-1': 2, 'vm-2': 4, 'vm-3': 0, 'vm-4': 1, 'vm-5': 1, 'vm-6': 2, 'vm-7': 0, 'vm-8': 2, 'vm-9': 5}


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
# HELP atlas_vm_backup_count_total VM Protection Groups total
# TYPE atlas_vm_backup_count_total counter
atlas_vm_backup_count_total{app_type="vmware",vm="vm-2"} 4.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-9"} 5.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-5"} 1.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-8"} 2.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-6"} 2.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-1"} 1.0
atlas_vm_backup_count_total{app_type="vmware",vm="vm-0"} 1.0
# HELP atlas_vm_backup_count_created VM Protection Groups total
# TYPE atlas_vm_backup_count_created gauge
atlas_vm_backup_count_created{app_type="vmware",vm="vm-2"} 1.6552055396272295e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-9"} 1.6552055416428018e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-5"} 1.6552055516652431e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-8"} 1.6552055536662025e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-6"} 1.655205557672574e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-1"} 1.655205561676035e+09
atlas_vm_backup_count_created{app_type="vmware",vm="vm-0"} 1.655205565676689e+09
"""