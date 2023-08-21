#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def delete_file(ds_name, remote_file_path):
        si = vcenter_utils.connect_vcenter()
        datacenter = None
        datastore = None
        for dc in si.content.rootFolder.childEntity:
            for ds in dc.datastore:
                if ds.name == ds_name:
                    datacenter = dc
                    datastore = ds

        file_manager = si.content.fileManager
        print(f'file_manager: {file_manager}')

        if not datacenter or not datastore:
            print("Could not find the datastore specified")
            raise SystemExit(-1)

        task = file_manager.DeleteDatastoreFile_Task(
            remote_file_path, datacenter)
        vcenter_utils.wait_for_task(task)


if __name__ == "__main__":
    datastore = "NIMBLE_VOL_DS3_17_GB"
    remote_file_path = "[NIMBLE_VOL_DS3_17_GB] orig_vm3/orig_vm3_1.vmdk"
    delete_file(datastore, remote_file_path)

    # https://communities.vmware.com/t5/vSphere-SDK-for-Java-Discussions/Is-there-an-API-to-rename-a-file-in-a-datastore/td-p/344268
