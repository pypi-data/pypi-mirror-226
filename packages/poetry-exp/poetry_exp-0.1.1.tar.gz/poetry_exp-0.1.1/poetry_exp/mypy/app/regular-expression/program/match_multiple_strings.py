import re

collect_map_result = """

2023-03-02 12:15:55,254.254 WARN: [NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect to peer. Error: Host address lookup for server ftc31-2s5 failed: Name or service not known
2023-03-02 12:15:55,254.254 WARN: [NFC ERROR]NfcEstablishAuthCnxToServer: Failed to create new AuthD connection: Host address lookup for server ftc31-2s5 failed: Name or service not known
2023-03-02 12:15:55,254.254 WARN: [NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect to peer. Error: Host address lookup for server ftc31-2s5 failed: Name or service not known
2023-03-13 00:00:29,146.146 NBD_ClientOpen: Couldn't connect to gl4dr-esxi02.zw.local:902 Failed to connect to server 10.10.10.28:902

2023-03-13 00:00:18,980.980 INFO: Attempting connection with vCenter 172.16.10.31

2023-03-13 00:00:29,146.146 [NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect to peer. Error: Failed to connect to server 10.10.10.28:902

2023-03-13 00:00:29,146.146 [NFC ERROR]Nfc_BindAndEstablishAuthdCnx3: Failed to create a connection with server 10.10.10.28: Failed to connect to server 10.10.10.28:902
8237262144287021352n:[NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect: Failed to connect to server 10.10.10.28:902
8237262144287021352n:Cnx_Connect: Error message: Failed to connect to server 10.10.10.28:902
2023-03-13 00:00:29,146.146 [NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect: Failed to connect to server 10.10.10.28:902
2023-03-13 00:00:29,146.146 [NFC ERROR]NfcNewAuthdConnectionEx: Failed to connect to peer. Error: Failed to connect to server 10.10.10.28:902
2023-03-13 00:00:29,146.146 [NFC ERROR]NfcEstablishAuthCnxToServer: Failed to create new AuthD connection: Failed to connect to server 10.10.10.28:902
983 ] executing vddk command ['/usr/lib64/hpe-atlas/vddk-manager/diskOperationExecutor', '-operation', 'getAllocMap', '-ip', '172.17.29.160', '-username', 'administrator@vsphere.local', '-virtualMachineMoRef', 'moref=vm-82', '-taskId', '87a43da0-3126-4093-a067-3091f0b396ca', '-requestId', 'req-a938101c-45ce-4372-bcaf-9f5d8b854983', '-snapShotMoRef', 'snapshot-3689', '-path', '[Nim811-VOL-DS4-17-GB] tvm1_1/tvm1.vmdk', '-vCenterId', 'd9434f8d-b8a0-44fc-b065-c5bce71a4093', '-deviceKey', '2000']
2023-03-06 06:08:59,413.413 29909 INFO hypervisor_apps.vmware_app.helpers.vddk_helper [req-a938101c-45ce-4372-bcaf-9f5d8b854983 ] Vddk operation: getAllocMap, result: 2023-03-06 06:08:52,143.143 INFO: Utils.cpp: loadAndInitializeLibrary: NA: NA: -839994848353179543: 30212n:Loading vddk library
2023-03-06 06:08:52,165.165 INFO: Utils.cpp: loadAndInitializeLibrary: NA: NA: 3385621917036980769: 30212n:Initializing VixDiskLib
2023-03-06 06:08:52,166.166 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:OBJLIB-LIB: Objlib initialized.
2023-03-06 06:08:52,166.166 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:VixDiskLib: Attempting to locate advanced transport module in "/usr/lib64/vddk8.0".
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:VixDiskLib: Could not load default plugins from /usr/lib64/vddk8.0/lib64/libdiskLibPlugin.so: Cannot open library: /usr/lib64/vddk8.0/lib64/libdiskLibPlugin.so: cannot open shared object file: No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:DictionaryLoad: Cannot open file "/etc/vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:[msg.dictionary.load.openFailed] Cannot open file "/etc/vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:PREF Optional preferences file not found at /etc/vmware/config. Using default values.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:DictionaryLoad: Cannot open file "/usr/lib/vmware/settings": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:[msg.dictionary.load.openFailed] Cannot open file "/usr/lib/vmware/settings": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:PREF Optional preferences file not found at /usr/lib/vmware/settings. Using default values.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:DictionaryLoad: Cannot open file "/usr/lib/vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:[msg.dictionary.load.openFailed] Cannot open file "/usr/lib/vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:PREF Optional preferences file not found at /usr/lib/vmware/config. Using default values.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:DictionaryLoad: Cannot open file "/home/vmware-app/.vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:[msg.dictionary.load.openFailed] Cannot open file "/home/vmware-app/.vmware/config": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:PREF Optional preferences file not found at /home/vmware-app/.vmware/config. Using default values.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:DictionaryLoad: Cannot open file "/home/vmware-app/.vmware/preferences": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:[msg.dictionary.load.openFailed] Cannot open file "/home/vmware-app/.vmware/preferences": No such file or directory.
2023-03-06 06:08:52,167.167 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:PREF Optional preferences file not found at /home/vmware-app/.vmware/preferences. Using default values.
2023-03-06 06:08:52,171.171 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:lib/ssl: OpenSSL using FIPS_drbg for RAND
2023-03-06 06:08:52,171.171 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:lib/ssl: protocol list tls1.2
2023-03-06 06:08:52,171.171 INF2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] Glibc malloc guards disabled.
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] Initialized SystemFactory
2023-03-06T06:08:52.345Z warning -[30212] [Originator@6876 sub=Default] Unrecognized log/level '' using 'info'
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] Logging uses fast path: true
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] The bora/lib logs WILL be handled by VmaCore
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] Initialized channel manager
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=Default] Current working directory: /
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=ThreadPool] Catch work item exceptions disabled.
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=FairScheduler] Priority level 4 is now active.
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=WorkQueue.vmacoreDefaultIOCompletionQueue] Created: WorkQueue.vmacoreDefaultIOCompletionQueue, type = fair, priority = 4, itemWeight = 1
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=FairScheduler] Priority level 8 is now active.
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=WorkQueue.vmacoreDefaultIOQueue] Created: WorkQueue.vmacoreDefaultIOQueue, type = fair, priority = 8, itemWeight = 1
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=FairScheduler] Priority level 16 is now active.
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=WorkQueue.vmacoreDefaultLongTaskQueue] Created: WorkQueue.vmacoreDefaultLongTaskQueue, type = fair, priority = 16, itemWeight = 1
2023-03-06T06:08:52.345Z info -[30212] [Originator@6876 sub=ThreadPool] Registered foreign worker - allocated: 1, idle: 0
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=ThreadPool] Registered foreign worker - allocated: 2, idle: 0
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=ThreadPool] Registered foreign worker - allocated: 3, idle: 0
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=ThreadPool] Registered foreign worker - allocated: 4, idle: 0
2023-03-06T06:08:52.346Z info -[30213] [Originator@6876 sub=ThreadPool] Entering worker thread loop
2023-03-06T06:08:52.346Z info -[30214] [Originator@6876 sub=ThreadPool] Entering worker thread loop
2023-03-06T06:08:52.346Z info -[30215] [Originator@6876 sub=ThreadPool] Entering worker thread loop
2023-03-06T06:08:52.346Z info -[30216] [Originator@6876 sub=ThreadPool] Entering worker thread loop
2023-03-06T06:08:52.346Z info -[30217] [Originator@6876 sub=ThreadPool] Entering IO thread loop
2023-03-06T06:08:52.346Z info -[30218] [Originator@6876 sub=ThreadPool] Entering IO thread loop
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=ThreadPool] Thread pool fair initial threads spawned. IO: 2, Min workers: 4, Max workers: 13, Reservation ratio: 9
2023-03-06T06:08:52.346Z info -[30219] [Originator@6876 sub=ThreadPool] Entering fair thread loop
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=Default] Syscommand enabled: true
2023-03-06T06:08:52.346Z info -[30212] [Originator@6876 sub=Default] ReaperManager Initialized
2023-03-06T06:08:55.393Z warning -[30220] [Originator@6876 sub=IO.Connection] Failed to connect; <io_obj p:0x00007f5288001d18, h:8, <TCP '172.17.81.18 : 60738'>, <TCP '172.17.29.160 : 443'>>, e: 113(No1 route to host), duration: 3004msec
2023-03-06T06:08:55.394Z warning -[30220] [Originator@6876 sub=HttpConnectionPool-000000] Failed to get pooled connection; <cs p:0000000001a26220, TCP:172.17.29.160:443>, (null), duration: 3005msec, N7Vmacore15SystemExceptionE(No route to host)
--> [context]zKq7AVECAQAAADkgOQEPLQAAaM1GbGlidm1hY29yZS5zbwAAb6UiAJISIQDNeRwAhPsvAKXdNQBm3jUANeY1AEnsNQAfpzAAbSYwAM1BMAA+hUEBpX4AbGlicHRocmVhZC5zby4wAAIN6w9saWJjLnNvLjYA[/context]
2023-03-06T06:08:55.396Z error -[30220] [Originator@6876 sub=IO.Http] User agent failed to send request; (null), N7Vmacore15SystemExceptionE(No route to host)
--> [context]zKq7AVECAQAAADkgOQEPLQAAaM1GbGlidm1hY29yZS5zbwAAb6UiAJISIQDNeRwAhPsvAKXdNQBm3jUANeY1AEnsNQAfpzAAbSYwAM1BMAA+hUEBpX4AbGlicHRocmVhZC5zby4wAAIN6w9saWJjLnNvLjYA[/context]
2023-03-06T06:08:58.399Z warning -[30228] [Originator@6876 sub=IO.Connection] Failed to connect; <io_obj p:0x00007f5288001d18, h:8, <TCP '172.17.81.18 : 60740'>, <TCP '172.17.29.160 : 443'>>, e: 113(No route to host), duration: 2999msec
2023-03-06T06:08:58.399Z warning -[30228] [Originator@6876 sub=HttpConnectionPool-000000] Failed to get pooled connection; <cs p:0000000001a25520, TCP:172.17.29.160:443>, (null), duration: 3000msec, N7Vmacore15SystemExceptionE(No route to host)
--> [context]zKq7AVECAQAAADkgOQEPLQAAaM1GbGlidm1hY29yZS5zbwAAb6UiAJISIQDNeRwAhPsvAKXdNQBm3jUANeY1AEnsNQAfpzAAbSYwAM1BMAA+hUEBpX4AbGlicHRocmVhZC5zby4wAAIN6w9saWJjLnNvLjYA[/context]
O: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:lib/ssl: protocol list tls1.2 (openssl flags 0x17000000)
2023-03-06 06:08:52,171.171 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:lib/ssl: cipher list ECDHE+AESGCM:RSA+AESGCM:ECDHE+AES:RSA+AES
2023-03-06 06:08:52,171.171 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:lib/ssl: curves list prime256v1:secp384r1:secp521r1
2023-03-06 06:08:52,203.203 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:VixDiskLib: Advanced transport module not loaded.
2023-03-06 06:08:52,203.203 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:VixDiskLib: Using transport modes from DiskLib: file:nbdssl:nbd.
2023-03-06 06:08:52,203.203 INFO: Logger.cpp: NA: NA: 3385621917036980769: 12601508078815311364n:VMware VixDiskLib (8.0.0) Release build-20521017
2023-03-06 06:08:52,347.347 INFO: diskOperationExecutor.cpp: getAllocationMap: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 30212n:Attempting connection with vCenter 172.17.29.160
2023-03-06 06:08:52,347.347 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_ConnectEx: Establish connection using (null).
2023-03-06 06:08:52,347.347 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLibConnectInt: Establish connection.
2023-03-06 06:08:52,347.347 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: Resolve host.
2023-03-06 06:08:55,398.398 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLibConnectInt: Failed to start session. Cannot get compatible version for vim at 6003.
2023-03-06 06:08:55,398.398 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_ConnectEx: No transport plugin. Advanced transports not available.
2023-03-06 06:08:55,398.398 INFO: diskOperationExecutor.cpp: doGetAllocatedBlocks: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 30212n:Attempting to open [Nim811-VOL-DS4-17-GB] tvm1_1/tvm1.vmdk disk
2023-03-06 06:08:55,398.398 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_OpenEx: Open a disk.
2023-03-06 06:08:58,402.402 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_OpenEx: Failed to start session. Cannot get compatible version for vim at 7403.
2023-03-06 06:08:58,402.402 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_Open: Cannot open disk [Nim811-VOL-DS4-17-GB] tvm1_1/tvm1.vmdk. Error 1 (Unknown error) at 7504.
2023-03-06 06:08:58,402.402 ERROR: diskOperationExecutor.cpp: doGetAllocatedBlocks: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 30212n:VixDiskLib_Open failed
2023-03-06 06:08:58,402.402 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_FreeConnectParams: Free connection parameters.
2023-03-06 06:08:58,403.403 INFO: diskOperationExecutor.cpp: main: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 30212n:Successfully completed getAllocMap operation
2023-03-06 06:08:58,403.403 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VDDK_PhoneHome: VDDK PhoneHome succeed to exit
2023-03-06 06:08:58,403.403 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:VixDiskLib: VixDiskLib_Exit: Unmatched Init calls so far: 1.
2023-03-06 06:08:59,403.403 INFO: Logger.cpp: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 12601508078815311364n:OBJLIB-LIB: ObjLib cleanup done.
2023-03-06 06:08:59,406.406 INFO: diskOperationExecutor.cpp: main: 87a43da0-3126-4093-a067-3091f0b396ca: req-a938101c-45ce-4372-bcaf-9f5d8b854983: 3385621917036980769: 30212n:return_code: 1
The server refused connection
Connection Failed

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
    r"\b|\bNo route to host"
    r"\b|\bThe server refused connection"
    r"\b|\bService Unavailable"
    r"\b|\bConnection Failed"
    r"\b")


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