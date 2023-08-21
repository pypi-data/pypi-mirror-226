#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from app.vmware_exp.examples import vcenter_utils


def move_vmdk(datacenter_name, remote_file_path, new_name):
    datacenter = vcenter_utils.lookup_object(vim.Datacenter, datacenter_name)
    print(datacenter)
    if not datacenter:
        print("Could not find the datastore specified")
        raise SystemExit(-1)

    si = vcenter_utils.connect_vcenter()
    vmdk_manager = si.content.virtualDiskManager
    print(f'vmdk_manager: {vmdk_manager}')

    task = vmdk_manager.MoveVirtualDisk_Task(
            remote_file_path, datacenter, new_name, datacenter)
    vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datacenter = "Datacenter1"
    remote_file_path= "[3PAR_VOl_3_TB] windowsServer/windowsServer_4.vmdk"
    new_name = "[3PAR_VOl_3_TB] windowsServer/windowsServer_4_bkp.vmdk"
    #
    # remote_file_path = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1_orig_bkp.vmdk"
    # new_name = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk"

    # datacenter = "ananya-dc"
    # remote_file_path = "[snap-7ec509eb-nimble-ds] NEW-NIMBLE-WINDOWS-clone10/NEW-NIMBLE-WINDOWS-clone10.vmdk"
    # new_name = "[snap-7ec509eb-nimble-ds] NEW-NIMBLE-WINDOWS-clone10/NEW-NIMBLE-WINDOWS-clone10_bkp.vmdk"
    # move_vmdk(datacenter, remote_file_path, new_name)

    datacenter = "ananya-dc"
    remote_file_path = "[datastore1] Atlas-24Oct/Atlas-24Oct.vmdk"
    new_name = "[datastore1] Atlas-24Oct/Atlas-24Oct_bkp.vmdk"
    move_vmdk(datacenter, remote_file_path, new_name)

    # https://communities.vmware.com/t5/vSphere-SDK-for-Java-Discussions/Is-there-an-API-to-rename-a-file-in-a-datastore/td-p/344268
