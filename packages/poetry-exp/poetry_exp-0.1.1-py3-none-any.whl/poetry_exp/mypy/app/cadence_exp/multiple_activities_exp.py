import sys
import logging
from cadence.activity_method import activity_method
from cadence.workerfactory import WorkerFactory
from cadence.workflow import workflow_method, Workflow, WorkflowClient

logging.basicConfig(level=logging.DEBUG)

TASK_LIST = "HelloActivity-python-tasklist"
DOMAIN = "sample"
DOMAIN = "test-domain"

# docker run --network=host --rm ubercadence/cli:master --do test-domain domain register -rd 1


# Activities Interface
class CollectMapActivities:
    @activity_method(task_list=TASK_LIST, schedule_to_close_timeout_seconds=2)
    def collect_map(self, vm_id: str, disk_path: str) -> str:
        raise NotImplementedError


# Activities Implementation
class CollectMapActivitiesImpl:
    def collect_map(self, vm_id: str, disk_path: str):
        print (f'Collecting the map for VM: {vm_id}, disk_path: {disk_path}')
        return disk_path


# Activities Interface
class CopyDiskActivities:
    @activity_method(task_list=TASK_LIST, schedule_to_close_timeout_seconds=2)
    def copy_disk(self, vm_id: str, disk_path: str) -> str:
        raise NotImplementedError


# Activities Implementation
class CopyDiskActivitiesImpl:
    def copy_disk(self, vm_id: str, disk_path: str):
        print(f'Copying the disk for VM: {vm_id}, disk_path: {disk_path}')
        return disk_path


# Workflow Interface
class BackupWorkflow:
    @workflow_method(execution_start_to_close_timeout_seconds=10, task_list=TASK_LIST)
    async def create_backup(self, vm_id: str, disk_path: str) -> str:
        raise NotImplementedError


# Workflow Implementation
class BackupWorkflowImpl(BackupWorkflow):

    def __init__(self):
        self.collect_map_activities: CollectMapActivities = Workflow.new_activity_stub(CollectMapActivities)
        self.copy_disk_activities: CopyDiskActivities = Workflow.new_activity_stub(CopyDiskActivities)

    async def create_backup(self, vm_id: str, disk_path: str):
        # Place any Python code here that you want to ensure is executed to completion.
        # Note: code in workflow functions must be deterministic so that the same code paths
        # are ran during replay.
        map = await self.collect_map_activities.collect_map(vm_id, disk_path)
        return await self.copy_disk_activities.copy_disk(vm_id, disk_path)


if __name__ == '__main__':
    factory = WorkerFactory("localhost", 7933, DOMAIN)
    worker = factory.new_worker(TASK_LIST)
    worker.register_activities_implementation(CollectMapActivitiesImpl(), "CollectMapActivities")
    worker.register_activities_implementation(CopyDiskActivitiesImpl(), "CopyDiskActivities")

    worker.register_workflow_implementation_type(BackupWorkflowImpl)
    factory.start()

    client = WorkflowClient.new_client(domain=DOMAIN)
    bkp_workflow: BackupWorkflow = client.new_workflow_stub(BackupWorkflow)
    result = bkp_workflow.create_backup("vm-1", "ds1/vm1.vmdk")
    print(result)

    print("Stopping workers....")
    worker.stop()
    print("Workers stopped...")
    sys.exit(0)