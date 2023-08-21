#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from app.vmware_exp.examples import vcenter_utils


def get_datastore_files(datastore_name, search_pattern="*.xml"):
    search_spec = vim.HostDatastoreBrowserSearchSpec(
        matchPattern=[search_pattern], searchCaseInsensitive=True)
    datastore_obj = vcenter_utils.lookup_object(vim.Datastore, datastore_name)
    print(f'datastore_obj: {datastore_obj}')
    ds_browser_ref = datastore_obj.browser
    print(f'ds_browser_ref: {ds_browser_ref}')

    search_task = ds_browser_ref.SearchDatastoreSubFolders_Task(
        datastorePath="[" + datastore_name + "]", searchSpec=search_spec)
    search_results = vcenter_utils.wait_for_task(search_task)
    print(search_results)
    for search_result in search_results:
        print(f'FolderPath: {search_result.folderPath}')
        for file_obj in search_result.file:
            print(f'file: {file_obj.path}')


def get_vm_files(datastore_name, search_in_vm, search_pattern=".xml"):
    files_with_search_pattern = []
    search_spec = vim.HostDatastoreBrowserSearchSpec(
        matchPattern=["*" + search_pattern], searchCaseInsensitive=True)
    datastore_obj = vcenter_utils.lookup_object(vim.Datastore, datastore_name)
    print(f'datastore_obj: {datastore_obj}')
    ds_browser_ref = datastore_obj.browser
    print(f'ds_browser_ref: {ds_browser_ref}')

    search_task = ds_browser_ref.SearchDatastoreSubFolders_Task(
        datastorePath="[" + datastore_name + "]", searchSpec=search_spec)
    search_results = vcenter_utils.wait_for_task(search_task)
    # print(search_results)
    for search_result in search_results:

        if not hasattr(search_result, 'file'):
            continue
        folder_path = None
        files = search_result.file
        for file in files:
            if hasattr(file, "path") and file.path:
                # ubuntu20.04.3_clone1-quiesce_manifest8.xml
                vm_name = file.path.rsplit("-quiesce_manifest")[0]  # ubuntu20.04.3_clone1
                print(f'vm_name: {vm_name}')
            if hasattr(search_result, "folderPath") and \
                    search_result.folderPath:
                # [NIm811-VOL-DS1-505-GB] Ubuntu-VM-25-GB/
                folder_path = search_result.folderPath.split()[1]   # Ubuntu-VM-25-GB/
                if folder_path and not folder_path.endswith("/"):
                    folder_path = folder_path + "/"
                print(f'folder_path: {folder_path}')

            print(f'search_in_vm: {search_in_vm==vm_name}')
            if search_in_vm == vm_name or file.path == search_in_vm + search_pattern:
                files_with_search_pattern.append(folder_path + file.path)

    print(files_with_search_pattern)  # ['ubuntu20.04.3_clone1/ubuntu20.04.3_clone1-quiesce_manifest10.xml', 'ubuntu20.04.3_clone1/ubuntu20.04.3_clone1-quiesce_manifest11.xml']


def get_vm_files_by_pattern(datastore_name, search_in_vm, search_pattern):
    files_with_search_pattern = []
    print(f'search_pattern: {search_pattern}')
    search_spec = vim.HostDatastoreBrowserSearchSpec(
        matchPattern=[search_pattern], searchCaseInsensitive=True)
    datastore_obj = vcenter_utils.lookup_object(vim.Datastore, datastore_name)
    print(f'datastore_obj: {datastore_obj}')
    ds_browser_ref = datastore_obj.browser
    print(f'ds_browser_ref: {ds_browser_ref}')

    search_task = ds_browser_ref.SearchDatastoreSubFolders_Task(
        datastorePath="[" + datastore_name + "]", searchSpec=search_spec)
    search_results = vcenter_utils.wait_for_task(search_task)
    # print(search_results)
    for search_result in search_results:

        if not hasattr(search_result, 'file'):
            continue
        files = search_result.file
        for file in files:
            if hasattr(file, "path") and hasattr(search_result, "folderPath"):
                # file.path: ubuntu20.04.3_clone1-quiesce_manifest8.xml
                # folder path: [NIm811-VOL-DS1-505-GB] Ubuntu-VM-25-GB/
                # [NIm811-VOL-DS1-505-GB] Ubuntu-VM-25-GB/
                vm_folder = search_result.folderPath.split()[1]   # Ubuntu-VM-25-GB/
                if vm_folder and not vm_folder.endswith("/"):
                    vm_folder = vm_folder + "/"
                files_with_search_pattern.append(vm_folder + file.path)

    print(files_with_search_pattern)  # ['ubuntu20.04.3_clone1/ubuntu20.04.3_clone1-quiesce_manifest10.xml', 'ubuntu20.04.3_clone1/ubuntu20.04.3_clone1-quiesce_manifest11.xml']



if __name__ == "__main__":
    datastore = "NIm811-VOL-DS1-505-GB"
    vitual_machine_name = "ubuntu20.04.3_clone1"
    file_search_pattern = vitual_machine_name + "-quiesce_manifest*.xml"
    #get_datastore_files(datastore)
    #get_vm_files(datastore, vitual_machine_name)
    #get_vm_files_by_pattern(datastore, vitual_machine_name, file_search_pattern)

    vitual_machine_name = "win2008_vvol_vm2"
    datastore = 'PRIMIRA_VVOL1'
    vss_file_search_pattern = vitual_machine_name + "-vss_manifests*.zip"  # win2016_server-vss_manifests1.zip
    get_vm_files_by_pattern(datastore, vitual_machine_name, vss_file_search_pattern)




"""

C:\Python3\python.exe "C:/Users/aafakmoh/OneDrive - Hewlett Packard Enterprise/mypy/app/vmware_exp/examples/browse_datastore_files.py"
C:\Python3\lib\site-packages\OpenSSL\crypto.py:12: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
  from cryptography import x509
connecting to vcenter...
connected, vcenter: %s 'vim.ServiceInstance:ServiceInstance'
datastore_obj: 'vim.Datastore:datastore-39005'
ds_browser_ref: 'vim.host.DatastoreBrowser:datastoreBrowser-datastore-39005'
Task done, result: (vim.host.DatastoreBrowser.SearchResults) [
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] small-ubuntu-vm/',   # For VVOL: [PRIMIRA_VVOL1] naa.60002AC0000000000001705700026282
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'small-ubuntu-vm-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   },
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] ubuntu20.04.3_clone1/',
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'ubuntu20.04.3_clone1-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   },
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] Ubuntu-VM-25-GB/',
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'Ubuntu-VM-25-GB-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   }
]
(vim.host.DatastoreBrowser.SearchResults) [
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] small-ubuntu-vm/',
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'small-ubuntu-vm-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   },
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] ubuntu20.04.3_clone1/',
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'ubuntu20.04.3_clone1-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   },
   (vim.host.DatastoreBrowser.SearchResults) {
      dynamicType = <unset>,
      dynamicProperty = (vmodl.DynamicProperty) [],
      datastore = 'vim.Datastore:datastore-39005',
      folderPath = '[NIm811-VOL-DS1-505-GB] Ubuntu-VM-25-GB/',
      file = (vim.host.DatastoreBrowser.FileInfo) [
         (vim.host.DatastoreBrowser.FileInfo) {
            dynamicType = <unset>,
            dynamicProperty = (vmodl.DynamicProperty) [],
            path = 'Ubuntu-VM-25-GB-aux.xml',
            friendlyName = <unset>,
            fileSize = <unset>,
            modification = <unset>,
            owner = <unset>
         }
      ]
   }
]

Process finished with exit code 0


"""