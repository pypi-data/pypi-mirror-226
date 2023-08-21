#!/usr/bin/env python

from __future__ import print_function  # This import is for python2.*
import atexit
import requests
import ssl

from pyVim import connect
from pyVmomi import vim

from vmware_exp.examples import vcenter_utils


def delete_file(ds_name, remote_file_path):
        service_instance = vcenter_utils.connect_vcenter()
        content = service_instance.RetrieveContent()

        # Get the list of all datacenters we have available to us
        datacenters_object_view = content.viewManager.CreateContainerView(
            content.rootFolder,
            [vim.Datacenter],
            True)

        # Find the datastore and datacenter we are using
        datacenter = None
        datastore = None
        for dc in datacenters_object_view.view:
            datastores_object_view = content.viewManager.CreateContainerView(
                dc,
                [vim.Datastore],
                True)
            for ds in datastores_object_view.view:
                if ds.info.name == ds_name:
                    datacenter = dc
                    datastore = ds
        if not datacenter or not datastore:
            print("Could not find the datastore specified")
            raise SystemExit(-1)
        # Clean up the views now that we have what we need
        datastores_object_view.Destroy()
        datacenters_object_view.Destroy()

        # Build the url to put the file - https://hostname:port/resource?params
        if not remote_file_path.startswith("/"):
            remote_file_path = "/" + remote_file_path
        else:
            remote_file_path = remote_file_path
        resource = "/folder" + remote_file_path
        params = {"dsName": datastore.info.name,
                  "dcPath": datacenter.name}
        print(f'.............params: {params}')
        http_url = "https://" + vcenter_utils.HOST + ":443" + resource

        # Get the cookie built from the current session
        client_cookie = service_instance._stub.cookie
        # Break apart the cookie into it's component parts - This is more than
        # is needed, but a good example of how to break apart the cookie
        # anyways. The verbosity makes it clear what is happening.
        cookie_name = client_cookie.split("=", 1)[0]
        cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
        cookie_path = client_cookie.split("=", 1)[1].split(";", 1)[1].split(
            ";", 1)[0].lstrip()
        cookie_text = " " + cookie_value + "; $" + cookie_path
        # Make a cookie
        cookie = dict()
        cookie[cookie_name] = cookie_text

        # Get the request headers set up
        headers = {'Content-Type': 'application/octet-stream'}
        print(f'...............http_url: {http_url}')


        # Connect and download the file
        response = requests.delete(http_url,
                               params=params,
                               headers=headers,
                               cookies=cookie,
                               verify=False)
        print(f'..........{response.text}')


if __name__ == "__main__":
    datastore = "NIMBLE_VOL_DS3_17_GB"
    remote_file_path= "orig_vm3/orig_vm3_1.vmdk"
    remote_file_path="orig_vm3/orig_vm3_1-flat.vmdk"
    delete_file(datastore, remote_file_path)
