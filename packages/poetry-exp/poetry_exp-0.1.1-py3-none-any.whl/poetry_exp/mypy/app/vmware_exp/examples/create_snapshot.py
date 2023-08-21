import vcenter_utils
from conf import constants

def create_snapshot(vm_name):
    si = vcenter_utils.connect_vcenter()
    print ('Creating snapshot....')
    vcenter_content = si.RetrieveContent()
    inventory_path = '{0}/vm/{1}'.format(constants.VCENTER_DATACENTER, vm_name)
    vm = vcenter_content.searchIndex.FindByInventoryPath(inventory_path)
    if vm:
        print ('Found the VM')
        task = vm.CreateSnapshot_Task(
            name=vm_name, description='Test snapshot', memory=True, quiesce=False)
        print (task)

    else:
        raise Exception('Cannot find the VM {}'.format(vm_name))

if __name__ == '__main__':
    create_snapshot('vrb')