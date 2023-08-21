#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def delete_vmdk(datacenter_name, remote_file_path):
        si = vcenter_utils.connect_vcenter()
        datacenter = vcenter_utils.lookup_object(vim.Datacenter, datacenter_name)
        print(datacenter)
        if not datacenter:
            print("Could not find the datastore specified")
            raise SystemExit(-1)

        vmdk_manager = si.content.virtualDiskManager
        print(f'vmdk_manager: {vmdk_manager}')
        task = vmdk_manager.DeleteVirtualDisk_Task(
            remote_file_path, datacenter)
        vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datacenter_name = "Datacenter1"
    remote_file_path = "[NIMBLE-VOL-DS1-15-GB] test_vm4/test_vm4_bkp.vmdk"
    delete_vmdk(datacenter_name, remote_file_path)

    # https://communities.vmware.com/t5/vSphere-SDK-for-Java-Discussions/Is-there-an-API-to-rename-a-file-in-a-datastore/td-p/344268
