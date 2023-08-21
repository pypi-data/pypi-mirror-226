__author__ = 'gowtamk'
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#from __future__ import print_function

import atexit
import ssl
from pyVmomi import vim

from pyVim.connect import SmartConnect, Disconnect

sslContext = ssl.create_default_context()
sslContext.check_hostname = False
sslContext.verify_mode = ssl.CERT_NONE

si = None
si = None

si = SmartConnect(host="172.17.29.81",
                    user="Administrator@vsphere.local",
                    pwd="12ISO*help",
                    port=443,
                    sslContext=sslContext)

print('Connected to vceneter')

atexit.register(Disconnect, si)


def find_vm(vm_name):
    vcenter_content = si.RetrieveContent()
    container = vcenter_content.viewManager.CreateContainerView(
        vcenter_content.rootFolder, [vim.VirtualMachine], True)
    vms = container.view
    for vm in vms:
        if vm_name == vm.name:
            return vm


def get_moref(managed_object_id, managed_object_type):
    """
    Construct Managed Object reference based on its ID and Type
    """
    method = getattr(vim, managed_object_type)
    mo_ref = method(managed_object_id)

    return mo_ref


def create_cbt_file_map(instance_uuid, device_key, file_path="/tmp/blockinfo", change_id="*", snap_moref=None):

    vm = si.content.searchIndex.FindByUuid(None, instance_uuid, True, True)

    if (vm.config.changeTrackingEnabled == False):
        print('Enabling CBT')
        vm_spec = vim.VirtualMachineConfigSpec()

        vm_spec.changeTrackingEnabled = True

        vm.ReconfigVM_Task(spec=vm_spec)
    print('CBT Enabled')

    desc = None
    startPosition = 0
    startOffset = 0
    length = 0
    offset = 0
    file = open(file_path, "w")

    #change_Id = "52 c0 28 23 94 a8 dd b7-3f 93 ec 7c 4a 1c 4e 90/7"
    change_Id = change_id
    device_key = device_key

    print('Finding snapshot')
    if snap_moref:
        snap_moref_obj = get_moref(snap_moref, "VirtualMachineSnapshot")
    else:
        print('Using current snapshot')
        snap_moref_obj = vm.snapshot.currentSnapshot
    print(snap_moref_obj)

    while(True):
        changes = vm.QueryChangedDiskAreas(
                                       snapshot=snap_moref_obj,
                                       deviceKey=device_key,
                                       startOffset=startOffset,
                                       changeId=change_Id)
        print(changes)
        if len(changes.changedArea) == 0:
            print('No changes detected, exiting')
            break

        for i in range(len(changes.changedArea)):
            length = changes.changedArea[i].length
            offset = changes.changedArea[i].start
            print("offset:" + str(offset) + " Length:" + str(length))
            file.write(str(offset) + "," + str(length) + "\n")

        startOffset = offset + length
        if startOffset >= changes.length:
            break

if __name__ == '__main__':
    # vm-3544 (aafak-cbt-vm)  - Saying A specified parameter was not correct: deviceKey'
    create_cbt_file_map(
        instance_uuid="503b9e6a-94ec-8762-d34a-eb3b0285a88f",
        device_key=2000,
        file_path="blockinfo2",
        change_id = "*"
    )
