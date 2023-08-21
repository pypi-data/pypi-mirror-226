"""
Using the OvfToll(ovftool.exe)
Executing the powershell script using subprocess.Popen

#log the parameters
Write-Output "VMName = $($VMName)"
Write-Output "HostName = $($HostName)"
Write-Output "vCenterIPaddress = $($VCenterIPaddress)"
Write-Output "vCenterUsername = $($VCenterUsername)"
Write-Output "vCenterPort = $($VCenterPort)"
Write-Output "OvaOvfSource = $($OvaOvfSource)"
Write-Output "Datastore = $($Datastore)"
Write-Output "diskStorageFormat = $($DiskStorageFormat)"
Write-Output "Cluster = $($Cluster)"
Write-Output "ResourcePool = $($ResourcePool)"
Write-Output "powerState = $($PowerState)"
Write-Output "ovfConfigKeys = $($OvfConfigKeys)"
Write-Output "ovfConfigValues = *********"
Write-Output "timeout = $($Timeout)"
"""

from subprocess import Popen, PIPE


def execute_cmd(cmd, timeout=10):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    rc = p.wait() # will wait for the process to finish and return the exit code
    print rc
    if rc == 0:
        for line in p.stdout:
            print line
    else:
        for line in p.stderr:
            print line


if __name__ == '__main__':
    #execute_cmd('powershell ls')
    execute_cmd('powershell .\powershell_script.ps1')