import json
import sys

data = [
    {
        "id": "d2173af7-9e7a-59d4-a973-978f3dc158e3",
        "instanceUuid": "5012f602-ff20-ffe1-1c14-81278393005f",
        "deleted": False,
        "appType": "VMware",
        "createdAt": "2020-12-14T05:29:47.615Z",
        "clone": True,
        "lastRefreshed": "2020-12-14T05:29:47.615Z",
        "name": "demo_clone2",
        "resourceName": "demo_clone2",
        "uid": "564d31e3-e9c9-10ab-1ae9-f62598d56753",
        "type": "VMFS",
        "networkAddress": "10.10.10.1",
        "guestInfo": {
        "name": "Ubuntu",
        "type": "Linux"
        },
        "computeInfo": {
            "memory_size": "8192",
            "num_cpu_cores": 2,
            "num_cpu_threads": 2
        },
        "powerState": "On",
        "vmConfigPath": "[snap-1e7910b7-3PAR_VOL_DS3] clone-atlas-dec3-2020/clone-atlas-dec3-2020.vmx",
        "state": "Ok",
        "stateReason": "Ok",
        "status": "Ok",
        "updatedAt": "2020-12-14T05:29:47.615Z",
        "cacheRefreshState": "Ok",
        "parentInfo": {
            "uid": "group-v10"
        },
        "resourcePoolInfo": {
            "moref": "resgroup-70"
        },
        "appInfo": {
            "vmware": {
                "moref": "vm-108",
                "datastoresInfo": [{
                    "id": "15238f03-c381-5506-ad9a-9741f231669a",
                    "name": "snap-1e7910b7-3PAR_VOL_DS3"
                }],
                "toolsInfo": {
                    "type": "guestToolsTypeOpenVMTools",
                    "version": "10336",
                    "status": "NotRunning"
                },
                "datacenterInfo": {
                    "moref": "datacenter-3",
                    "name": "Datacenter1"
                }
            }
        },
        "hypervisorManagerInfo": {
            "id": "8da4e043-76df-4d44-8e97-4925979bb64f",
            "name": "VMware vCenter Server"
        },
        "hypervisorHostInfo": {
            "id": "cc11c15b-ff33-5658-8430-cb996243eb25",
            "name": "172.17.6.102"
        },
        "networksInfo": [{
            "id": "f74582a0-ee62-5339-b832-8b6bd725f1c1",
            "name": "VM Network"
        }],
        "cloneInfo": {
            "parentVMInfo": {
                "name": "clone-atlas-dec3-2020",
                "id": "1f498834-7d53-59b8-9540-4379790383fc"
            },
            "sourceSnapshotInfo": {
                "name": "vm-snap3",
                "id": "bf77219d-e2e4-4f2e-93aa-009bc5926197"
            },
            "sourceVMInfo": {
                "name": "clone-atlas-dec3-2020",
                "id": "1f498834-7d53-59b8-9540-4379790383fc"
            }
        }
    }

] *20000
#print(data)
print(f'Memory Size of data: {sys.getsizeof(data)}')  # 44
json_str = json.dumps(data)
#print(json_str)
#print(type(json_str))
print(f'Length of json string: {len(json_str)}')  # 174 char
print(f'Memory Size of json string: {sys.getsizeof(json_str)}')  # 199
print(f'Size of json string: {len(json_str.encode("utf-8"))}')  # 174 bytes

MAX_JSON_SIZE = 128 * 1024 * 1024  #(134217728)bytes


def publish_in_batches(events, batch_size):
    published_events = []
    event_counts = len(events)
    print(f'...Events # {event_counts}')
    print(f'...Batch size # {batch_size}')
    count = 0
    while count < event_counts:
        start_index = count
        end_index = count + batch_size
        if end_index > event_counts:
            print('End index exceeds the number')
            end_index = event_counts
        print(f'Batching from : [{start_index}:{end_index}]')

        batch = events[start_index:end_index]

        batch_json_size = len(json.dumps(batch))
        print(f'Batch json size : {batch_json_size} ')

        if batch_json_size > MAX_JSON_SIZE and len(batch) > 1:
            print(f'Batch size: {batch_json_size} bytes exceeds the max size: {MAX_JSON_SIZE} bytes, Re-batching')
            publish_in_batches(batch, len(batch)//2)

        published_events.extend(batch)
        count += batch_size

    return published_events

published_events = publish_in_batches(data, 10000)

# print(f'Published: {len(published_events)}')
# print(f'Published: {published_events}')

"""
For 50K docs:
Memory Size of data: 200036
Length of json string: 87200000
Memory Size of json string: 87200025
Size of json string: 87200000
Sending in one chunk


FOR 10K:
Memory Size of data: 40036
Length of json string: 17440000  # 17 MB
Memory Size of json string: 17440025
Size of json string: 17440000
Sending in one chunk


Memory Size of data: 80036
Length of json string: 34880000  # 35MB
Memory Size of json string: 34880025
Size of json string: 34880000
...Events # 20000
...Batch size # 10000
Batching from : [0:10000]
Batch json size : 17440000 
Batching from : [10000:20000]
Batch json size : 17440000 
"""