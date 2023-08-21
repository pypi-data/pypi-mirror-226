#deployVM.ps1

#------------------------------------------------------------------------------
# Copyright (C) 2016-2017 EMC Corporation. All Rights Reserved.
#------------------------------------------------------------------------------


#Description: This powershell script uses powercli to deploy VM
<#
.Description : Script  for deploying VM using ova.
    .Parameter $VMName: Name of the new VM to create
    .Parameter $HostName: ESXi host name
    .Parameter $VCenterIPaddress: vCenter IP or FQDN
    .Parameter $VCenterUsername: vCenter username
    .Parameter $VCenterPassword: vCenter password
    .Parameter $VCenterPort: vCenter port
    .Parameter $OvaOvfSource: Path of ova source file.
    .Parameter $Datacenter: Datacenter name.
    .Parameter $Datastore: vCenter datastore name
    .Parameter $DiskStorageFormat: Virtual disk format to be set (Thin2GB/Thick/Thick2GB/Thin/EagerZeroedThick)
    .Parameter $Cluster: vCenter cluster name
    .Parameter $ResourcePool: vCenter resource pool name
    .Parameter $OvfConfigKeys: Ova file configuration keys
    .Parameter $OvfConfigValues: Values for configuration keys of ova file
    .Parameter $PowerState: Post power state of new VM ("ON"/"OFF")
    .Parameter $IsvApp: Flag stating that vApp is to be deployed
    .Parameter $Timeout: Max time to wait for the deploy VM task.
    .Parameter $ExecutableDir: PowerCLI directory path.
    .Parameter $DeploymentType: Type of deployment powercli\ovftool
#>


param(
    [String] $VMName,
    [String] $HostName,
    [String] $VCenterIPaddress,
    [String] $VCenterUsername,
    [String] $VCenterPassword,
    [Int] $VCenterPort,
    [String] $OvaOvfSource,
    [String] $Datacenter,
    [String] $Datastore,
    [String] $DiskStorageFormat,
    [String] $Cluster,
    [String] $ResourcePool,
    [array] $OvfConfigKeys,
    [array] $OvfConfigValues,
    [String] $PowerState,
    [switch] $IsvApp,
    [Int] $Timeout,
    [String] $ExecutableDir,
    [String] $DeploymentType
)

function hexSpecialChars($inputString){
    foreach ($charelem in $inputString.ToCharArray()){
        if($charelem -match '[^a-zA-Z0-9]'){
            $cbyte = [Text.Encoding]::UTF8.GetBytes($charelem)
            $d = "%"+[System.BitConverter]::ToString($cbyte)
            $inputString = $inputString.replace([String]$charelem,$d)
        }
    }
    return $inputString
}

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

if($DeploymentType -eq 'powercli')
{
    #Naviagte to powercli
    cd $ExecutableDir
    Add-PSSnapin "VMware.VimAutomation.Core" | Out-Null

    #Connect to VI Server
    try{
        Write-Output "Connect to VI Server"
        $serverConnection = Connect-VIServer -Server $VCenterIPaddress -Protocol https -User $VCenterUsername `
        -Password $VCenterPassword -Port $VCenterPort -ErrorAction Stop
        }
    catch{
        return $_
    }

    Try{
        #get host and cluster objects
        Write-Output "get host and cluster objects"
        $cluster = Get-Cluster -Name $Cluster
        $vmHost = Get-VMHost -Name $HostName
        $location = $cluster
        if ($ResourcePool)
        {
            $resourcePoolObj = Get-ResourcePool -Location $cluster -Name $ResourcePool
            if ($resourcePoolObj)
            {
                $location = $resourcePoolObj
            }
        }

        Write-Output "cluster $($cluster)"
        Write-Output "resource pool $($resourcePoolObj)"
        Write-Output "host $($vmHost)"

        # Load OVF/OVA configuration into a variable
        $ovfconfig = Get-OvfConfiguration $OvaOvfSource
        # If custom ovf properties are specified, set properties with the provided values
        if ($OvfConfigKeys.length -gt 0){
            # Iterate over each property and assign the values
            ForEach ($key In $OvfConfigKeys) {
                $command = '$ovfconfig'
                $command = $command + '.' + $key
                $index = $OvfConfigKeys.IndexOf($key)
                $command = $command + ' = $OvfConfigValues[$index]'
                $message = "Setting property {0}" -f $key
                Write-Output $message
                invoke-Expression $command
            }
        }

        #deploy the VM
        Write-Output "deploy the VM"
        if ($location)
        {
            $deployTask = Import-VApp -Name $VMName -VMHost $vmHost -Source $OvaOvfSource -OvfConfiguration $ovfconfig `
            -Datastore $Datastore -DiskStorageFormat $DiskStorageFormat -Location $location -Force `
            -RunAsync:$true -ErrorAction Stop
        }
        else
        {
            $deployTask = Import-VApp -Name $VMName -VMHost $vmHost -Source $OvaOvfSource -OvfConfiguration $ovfconfig `
            -Datastore $Datastore -DiskStorageFormat $DiskStorageFormat -Force `
            -RunAsync:$true -ErrorAction Stop
        }

        #Loop till deploy vm object state not equal to success and time less than timeout
        $counter = 0
        Write-Output "loop till deploy vm object state not equal to success and time less than timeout $($Timeout)"
        while ($deployTask.State -ne "Success" -and $counter -lt $Timeout)
        {
            $counter = $counter + 1
            Start-Sleep(1)

            #Print the object info
            if($deployTask.State -eq "Error"){
                Write-Error $deployTask.TerminatingError
                return
            }

            #Stop the task if time is almost up
            if($counter -eq ($Timeout - 1))
            {Write-Output "Stopping the Task due to timeout."
                Stop-Task -Task $deployTask -Confirm:$false
            exit}
        }
        Write-Output "State = $($deployTask.State)"
        if($counter -ge $Timeout)
        {
            Write-Output "Stoping the Task outside of main loop. Timeout Reached"
            Stop-Task -Task $deployTask -Confirm:$false
            Write-Error "Timeout occurred while deploying Virtual Machine"
            exit
        }
        #Print the object info
        $deployTask
        if ($PowerState -eq "ON"){
            if ($IsvApp){
                Write-Output "Powering on Virtual App"
                Get-VApp -Name $VMName | Start-VApp
            }
            else{
                Write-Output "Powering on Virtual Machine"
                Get-VM -name $VMName | Start-VM -Confirm:$false -RunAsync
            }
        }
        Disconnect-VIServer -Server $serverConnection -Force -confirm:$false
    }
    Catch{
        Disconnect-VIServer -Server $serverConnection -Force -confirm:$false
        return $_
    }
}
else{
    # convert special chars in username and password to %<hex> format
    $VCenterUsername = hexSpecialChars($VCenterUsername)
    $VCenterPassword = hexSpecialChars($VCenterPassword)

    $argumentsPrefix = ' --X:logToConsole --noSSLVerify --acceptAllEulas --hideEula --name=' + $($VMName) +
    ' --datastore='+ $($Datastore) + ' --diskMode=' + $($DiskStorageFormat)
    if ($PowerState -eq "ON"){
        $argumentsPrefix = $argumentsPrefix + ' --powerOn '
    }
    $properties = ''
    if ($OvfConfigKeys.length -gt 0){
            # Iterate over each property and assign the values
            ForEach ($key In $OvfConfigKeys) {
                $commandSplit = $key.split(":")
                $index = $OvfConfigKeys.IndexOf($key)
                if ($commandSplit[1]){
                    $properties = $properties + ' {0}:"{1}"="{2}"' -f $commandSplit[0], $commandSplit[1],
                    $OvfConfigValues[$index]
                }
                else{
                    $properties = $properties + ' {0}={1}' -f $commandSplit[0], $OvfConfigValues[$index]
                }
            }
    }

    #$arguments = $arguments + ' ""{0}""' -f $OvaOvfSource
    $ovaPath = '"{0}"' -f $OvaOvfSource
    Write-Output "OVA Path supplied is,"
    $ovaPath
    $VIString = ' vi://' + $($VCenterUsername) + ':' + $($VCenterPassword) + '@' + $($VCenterIPaddress) + '/' +
    $($Datacenter) +'/host/'+ $($Cluster)
    $VILogString = ' vi://' + $($VCenterUsername) +':vCenterPassword@'+ $($VCenterIPaddress) + '/' +
    $($Datacenter) +'/host/'+ $($Cluster)
    if ($ResourcePool)
    {
        $poolString = '/Resources/'+ $($ResourcePool)
        $VIString = $($VIString) + $($poolString)
        $VILogString = $($VILogString) + $($poolString)
    }
    Write-Output "Connection string is,"
    $VILogString
    $scriptPath = '"{0}\ovftool.exe"' -f $ExecutableDir.Trim()
    Write-Output "OVFTOOL executable path,"
    $scriptPath
    Write-Output "Prefix parameters are,"
    $argumentsPrefix
    Write-Output "Starting deploying ova..."
    $job = Start-Job -ScriptBlock {
                    $cmd = '& {0} {1} {2} {3} {4}' -f $args[0],  $args[1], $args[2], $args[3], $args[4]
                    Invoke-Expression $cmd
                    } -ArgumentList $scriptPath, $argumentsPrefix, $properties, $ovaPath, $VIString
    $counter = 0
    while($counter -lt $Timeout){
        $counter = $counter + 1
	    Start-Sleep(1)
	    $output = Receive-Job $job
	    $output
        if($job.State -eq 'Completed'){
            $lastoutput = Receive-Job $job
            if (-not $lastoutput){
                if ($output -like '*Completed with errors*'){
                    Write-Error "Error deploying ova."
                }
            }
            else{
                $lastoutput
                if ($lastoutput -like '*Completed with errors*'){
                    Write-Error "Error deploying ova."
                }
            }
            return
        }
	    #Stop the task if time is almost up
	    if($counter -eq ($Timeout - 1)){
	        Stop-Job $job -Confirm:$false
	        Receive-Job $job
	        Write-Error "Timeout occurred while deploying Virtual Machine"
            return
        }
    }
    Remove-Job $job
}
