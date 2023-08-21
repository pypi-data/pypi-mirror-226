import re

collect_map_result = """
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:CnxOpenTCPSocket: Cannot connect to server 172.16.21.219:902: No route to host
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:CnxAuthdConnect: Returning false because CnxAuthdConnectTCP failed
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:CnxConnectAuthd: Returning false because CnxAuthdConnect failed
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:Cnx_Connect: Returning false because CnxConnectAuthd failed
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:Cnx_Connect: Error message: Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 WARN: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:[NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect: Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 WARN: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:[NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect to peer. Error: Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 WARN: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:[NFC ERROR]NfcEstablishAuthCnxToServer: Failed to create new AuthD connection: Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 WARN: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:[NFC ERROR]Nfc_BindAndEstablishAuthdCnx3: Failed to create a connection with server 172.16.21.219: Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:NBD_ClientOpen: Couldn't connect to 172.17.6.219:902 Failed to connect to server 172.16.21.219:902
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:DISKLIB-DSCPTR: DescriptorOpenNbd: Failed to open NBD extent 'vpxa-nfc://[NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk@{nfcip:172.16.21.219,hostname:172.17.6.219}:902': NBD_ERR_NETWORK_CONNECT
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:DISKLIB-LINK  : "vpxa-nfc://[NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk@{nfcip:172.16.21.219,hostname:172.17.6.219}:902" : failed to open (NBD_ERR_NETWORK_CONNECT).
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:DISKLIB-CHAIN : DiskChainOpen: "vpxa-nfc://[NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk@{nfcip:172.16.21.219,hostname:172.17.6.219}:902": failed to open: NBD_ERR_NETWORK_CONNECT.
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:DISKLIB-LIB   : Failed to open 'vpxa-nfc://[NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk@{nfcip:172.16.21.219,hostname:172.17.6.219}:902' with flags 0xe NBD_ERR_NETWORK_CONNECT (2338).
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: Detected DiskLib error 2338 (NBD_ERR_NETWORK_CONNECT).
2023-03-20 17:25:55,964.964 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: Failed to open disk vpxa-nfc://[NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk@{nfcip:172.16.21.219,hostname:172.17.6.219}:902!52 21 d6 65 db 6d 07 6e-26 5f 0a c0 dd b4 d7 6f. Error 14009 (The server refused connection) (DiskLib error 2338: NBD_ERR_NETWORK_CONNECT) at 6764.
2023-03-20 17:25:55,969.969 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: VixDiskLib_OpenEx: Cannot open disk [NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk. Error 14009 (The server refused connection) (DiskLib error 2338: NBD_ERR_NETWORK_CONNECT) at 7426.
2023-03-20 17:25:55,969.969 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: VixDiskLib_Open: Cannot open disk [NFS_Share_NetApp] CN-NFS-VM1/CN-NFS-VM1_4.vmdk. Error 14009 (The server refused connection) at 7504.
2023-03-20 17:25:55,969.969 ERROR: diskOperationExecutor.cpp: doGetAllocatedBlocks: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 20514n:VixDiskLib_Open failed
2023-03-20 17:25:55,969.969 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: VixDiskLib_FreeConnectParams: Free connection parameters.
2023-03-20 17:25:55,969.969 INFO: diskOperationExecutor.cpp: main: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 139723876093986n:Successfully completed getAllocMap operation
2023-03-20 17:25:55,969.969 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VDDK_PhoneHome: VDDK PhoneHome succeed to exit
2023-03-20 17:25:55,969.969 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:VixDiskLib: VixDiskLib_Exit: Unmatched Init calls so far: 1.
2023-03-20 17:25:56,970.970 INFO: Logger.cpp: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 3282006934344978466n:OBJLIB-LIB: ObjLib cleanup done.
2023-03-20 17:25:56,972.972 INFO: diskOperationExecutor.cpp: main: 72f62e12-aef2-45bf-9aab-05e66ecff9f6: req-81810f31-d222-4251-a7bb-29ea5da40254: -5687556580215790410: 139723876093986n:return_code: 14009

2023-03-20 17:25:56,980.980 19951 INFO hypervisor_apps.vmware_app.helpers.vddk_helper [req-81810f31-d222-4251-a7bb-29ea5da40254 ] Vddk operation: getAllocMap, error_code: 0, error: Error: The server refused connection

2023-03-20 17:25:56,981.981 19951 ERROR hypervisor_apps.vmware_app.helpers.vddk_helper [req-81810f31-d222-4251-a7bb-29ea5da40254 ] Calling_getAllocMap_Failed on VM: vm-3984. error code: 0, Error: The server refused connection


"""

# VDDK_ERR_PATTERNS = re.compile(
#     r"\bFailed to get pooled connection.*No route to host1"
#     r"\b|\bNo route to host1"
#     r"\b|\bThe server refused connection1"
#     r"\b|\bConnection Failed1"
#     r"\b|\bHost address lookup for server.*Name or service not known"
#     r"\b|\bCouldn't connect to.*Failed to connect to server1.*"
#     r"\b|\bFailed to connect to server1 .*902"
#     r"\b")

VDDK_CONNECTION_ERR_PATTERNS = re.compile(
    r"\bHost address lookup for server.*Name or service not known"
    r"\b|\bCouldn't connect to.*Failed to connect to server.*902"
    r"\b|\bCouldn't connect to.*Failed to connect to server.*"
    r"\b|\bFailed to connect to server.*902"
    r"\b|\bFailed to connect to server.*"
    r"\b|\bCannot connect to server.*No route to host"
    r"\b|\bNo route to host"
    r"\b|\bThe server refused connection"
    r"\b|\bService Unavailable"
    r"\b|\bConnection Failed"
    r"\b")

"""
Cannot connect to server 172.16.21.219:902: No route to host
"""

def format_no_route_host_err(err_str):
    """
    err_string exp:
    Failed to get pooled connection; <cs p:0000000001a26220, TCP:172.17.29.160:443>,
     (null), duration: 3005msec, N7Vmacore15SystemExceptionE(No route to host
    :param err_str:
    :return:
    """
    if 'No route to host' in err_str:
        err_msg = "No route to host"
        try:
            tcp_index = err_str.index("TCP:")
            ip_port_end_index = err_str.index(">,")
            ip_address = err_str[tcp_index+4: ip_port_end_index]
            print(ip_address)  # 172.17.29.160:443
            err_msg = "No route to host. Failed to connect to server 172.17.29.160:443"
        except Exception as e:
            print(e)

    print(err_msg)


if __name__ == '__main__':

    # matches = re.findall(VDDK_ERR_PATTERNS, collect_map_result)
    # if matches:
    #     print(f'String: matches: {matches}')
    # else:
    #     print(f'String: not matched')
    GEN_EXC = Exception
    match = VDDK_CONNECTION_ERR_PATTERNS.search(collect_map_result)
    if match:
        error = match.group()
        #format_no_route_host_err(error)
        print(f'String: matches: {error}, type: {type(error)}')
        raise GEN_EXC("Raising")
    else:
        print(f'String: not matched')