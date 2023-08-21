from app.vmware_exp.examples.conf import constants
import vcenter_utils
from datetime import datetime
from pyVmomi import vim, vmodl
from app.vmware_exp.examples import vcenter_utils


# https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/linked_clone.py
def take_snapshot(
        vm, snap_name='TestSnap-'+str(datetime.now()),
        quiesce=True, memory=False, description=None):
    # memory: Snapshot the virtual machines's memory
    # quiesce: quiesce the guest file system
    print(f'Taking snapshot of VM: {vm.name}')

    task = vm.CreateSnapshot_Task(
        name=snap_name, description=description,
        memory=memory, quiesce=quiesce)
    return vcenter_utils.wait_for_task(task)


def create_linked_clone(dc_name, vm_or_template_name, vm_name, snap_obj):
    print(f'Creating linked clone from VM/Template: {vm_or_template_name}')
    template = vcenter_utils.lookup_object(vim.VirtualMachine, vm_or_template_name)
    print (template)
    dest_folder = vcenter_utils.lookup_object(
        vim.Datacenter, dc_name)

    relocate_spec = vim.vm.RelocateSpec()
    relocate_spec.diskMoveType = 'createNewChildDiskBacking' # This is important for linked clone
    """
    this is the only properties of the entire script that will change your
    VM from a full clone to a linked clone. This property will create a new child
     disk on the destination datastore. This will be a snapshot of the read only original VMDK.
    """

    clone_spec = vim.vm.CloneSpec()
    clone_spec.template = False
    clone_spec.location = relocate_spec
    clone_spec.snapshot = snap_obj

    task = template.Clone(
        folder = dest_folder.vmFolder, name=vm_name, spec=clone_spec)
    result = vcenter_utils.wait_for_task(task)
    print(f'Successfully created the linked clone, result: {result}')


def create_clone2(vm_or_template_name, vm_name,
                  vm_folder=None, datastore_name=None,
                  resource_pool_name=None):
    template = vcenter_utils.lookup_object(vim.VirtualMachine, vm_or_template_name)

    data_center = vcenter_utils.lookup_object(vim.Datacenter, constants.VCENTER_DATACENTER)
    if vm_folder:
        dest_folder = vcenter_utils.lookup_object(vim.Folder, vm_folder)
    else:
        dest_folder = data_center.vmFolder

    if datastore_name:
        datastore = vcenter_utils.lookup_object([vim.Datastore], datastore_name)
    else:
        datastore = vcenter_utils.lookup_object([vim.Datastore], template.datastore[0].info.name)

    cluster = vcenter_utils.lookup_object(vim.ClusterComputeResource, constants.VCENTER_CLUSTER)

    if resource_pool_name:
        resource_pool = vcenter_utils.lookup_object(vim.ResourcePool, resource_pool_name)
    else:
        resource_pool = cluster.resourcePool

    relocate_spec = vim.vm.RelocateSpec()
    relocate_spec.datastore = datastore
    relocate_spec.pool = resource_pool

    clone_spec = vim.vm.CloneSpec()
    clone_spec.location = relocate_spec

    task = template.Clone(folder=dest_folder, name=vm_name, spec=clone_spec)
    result = vcenter_utils.wait_for_task(task)
    print (result)





if __name__ == '__main__':

    # vm = vcenter_utils.lookup_object_by_moref(vim.VirtualMachine, 'vm-40014')
    # print(vm)  # 'vim.VirtualMachine:vm-40014'
    virtual_machine_name = 'win2016_server'
    linked_clone_vm_name = 'win2016_server_linked_clone1'

    datacenter_name = 'Datacenter1'
    virtual_machine_name = 'win2008_vvol_vm2'
    linked_clone_vm_name = 'win2008_vvol_vm2_linked_clone2'
    vm = vcenter_utils.lookup_object(vim.VirtualMachine, virtual_machine_name)
    print(f'VM: {vm}')

    snapshot = take_snapshot(vm)
    snap_moref = snapshot._moId
    print(f'snap_moref: {snap_moref}')

    snapshot = vcenter_utils.get_moref('VirtualMachineSnapshot', snap_moref)
    create_linked_clone(datacenter_name, virtual_machine_name, linked_clone_vm_name, snapshot)

    # create_clone2(virtual_machine_name, 'linked_clone_vm1',
    #               vm_folder=constants.VCENTER_VM_FOLDER,
    #               datastore_name=constants.VCENTER_DATASTORE,
    #               resource_pool_name=constants.VCENTER_RESOURCE_POOL)



"""
https://room28.it/index.php/2016/11/24/use-linked-clone-instead-of-full-clone-to-create-vms/

https://docs.vmware.com/en/vCenter-Converter-Standalone/6.2/com.vmware.convsa.guide/GUID-93894315-EFCA-4DD8-B583-FA24272DA180.html
A linked clone is a copy of a virtual machine that shares virtual disks with the parent virtual machine
in an ongoing manner. A linked clone is a fast way to convert and run a new virtual machine.
You can create a linked clone from the current state, or snapshot, of a powered off virtual machine.
 This practice conserves disk space and lets multiple virtual machines use the same software installation.

All files available on the source machine at the moment of the snapshot continue to remain available
 to the linked clone. Ongoing changes to the virtual disk of the parent do not affect the linked clone,
  and changes to the disk of the linked clone do not affect the source machine.

A linked clone must have access to the source. Without access to the source, you cannot use a linked clone.

Full clone:
VM================================================>clone VM
disk1(10GB)   Entire disk copied                  Disk1(10 GB)
              Independent VM
            
LInked clone:
VM================================================>clone VM
|                                                   |
Delta           No disk copied                      Delta Refernig the Base disk
|                                               '
disk1(10GB)............................................                     
                        
            
The clone is not based on the VM but on a snapshot of the VM. Yes, you understood well.
This means you do not clone the full VMDK anymore, you just clone the snapshot,
which uses only a few KBytes. This is why this is so fast, and this is why it consumes so few space.


As you understood, the linked clone process will just spawn a new snapshot based
on the root VMDK of your template. The new created delta disk will refer to the template Read Only disk.

As you can see, you save the space of the template and as you just span a delta disk (same way as a VM snapshot),
you also save space.


 you use the VirtualMachineRelocateSpec object to specify where your virtual machine will be deployed.
You need the datastore view as well as the resource pool view. There is a property in this object
named diskMoveType which can have several values. The one I specified by default is
moveAllDiskBackingsAndAllowSharing. This means that all VM VMDK are copied onto the target
datastore and the snapshot mounted on this VMs from other VMs will remained a snapshot. You can find all the options


We are going to focus on the createNewChildDiskBacking option. Indeed, this is the only properties
of the entire script that will change your VM from a full clone to a linked clone.

This property will create a new child disk on the destination datastore. This will be a snapshot of
the read only original VMDK.

you create a clone based on a snapshot. You will need to take a snapshot of your template to make it real.
you will create Linked Clone, save a few space on your datastore and you will create VMs in a couple of seconds.
"""