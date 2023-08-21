#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def rename_file(datacenter_name, remote_file_path, new_name):
    datacenter = vcenter_utils.lookup_object(vim.Datacenter, datacenter_name)
    print(datacenter)
    if not datacenter:
        print("Could not find the datastore specified")
        raise SystemExit(-1)

    si = vcenter_utils.connect_vcenter()
    file_manager = si.content.fileManager
    print(f'file_manager: {file_manager}')

    task = file_manager.MoveDatastoreFile_Task(
        remote_file_path, datacenter, new_name, datacenter)
    vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datacenter = "Datacenter1"
    remote_file_path= "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk"
    new_name = "[NIMBLE_VOL_DS1_15_GB] abc_vm1/abc_vm1.vmdk_orig_bkp"
    rename_file(datacenter, remote_file_path, new_name)

    # https://communities.vmware.com/t5/vSphere-SDK-for-Java-Discussions/Is-there-an-API-to-rename-a-file-in-a-datastore/td-p/344268
