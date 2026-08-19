#!powershell

#AnsibleRequires -CSharpUtil Ansible.Basic
#Requires -Module VMware.PowerCLI

$spec = @{
    options = @{
        host = @{ type = "str"; required = $true }
        username = @{ type = "str"; required = $true }
        password = @{ type = "str"; required = $true; no_log = $true }
        datastore_name = @{ type = "str"; required = $true }
        file_path = @{ type = "path"; required = $true }
        destination_path = @{ type = "str"; required = $true }
        validate_certs = @{ type = "bool"; default = $true }
    }
    supports_check_mode = $false
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

function Upload-FileToVCenter {
    [CmdletBinding()]
    param (
        [string]$VCenterServer,
        [string]$VCenterUsername,
        [string]$VCenterPassword,
        [string]$DatastoreName,
        [string]$FilePath,
        [string]$DestinationPath,
        [bool]$ValidateCerts
    )

    try {
        if (-not $ValidateCerts) {
            Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false | Out-Null
        }

        Connect-VIServer -Server $VCenterServer -User $VCenterUsername -Password $VCenterPassword -ErrorAction Stop

        $datastore = Get-Datastore -Name $DatastoreName -ErrorAction Stop

        if (-not (Test-Path $FilePath)) {
            throw "File not found at path: $FilePath"
        }

        $driveName = "DS_" + [Guid]::NewGuid().ToString("N")
        New-PSDrive -Name $driveName -PSProvider VimDatastore -Root "\" -Location $datastore | Out-Null

        try {
            $fullDestinationPath = Join-Path -Path "$($driveName):\" -ChildPath $DestinationPath
            $fileExists = Test-Path $fullDestinationPath

            $sourceHash = (Get-FileHash -Path $FilePath -Algorithm SHA256).Hash

            if ($fileExists) {
                $tempPath = [System.IO.Path]::GetTempFileName()
                Copy-DatastoreItem -Item $fullDestinationPath -Destination $tempPath
                $destHash = (Get-FileHash -Path $tempPath -Algorithm SHA256).Hash
                Remove-Item -Path $tempPath -Force

                if ($sourceHash -eq $destHash) {
                    return @{
                        changed = $false
                        msg = "File already exists with the same content"
                        file_name = (Split-Path $FilePath -Leaf)
                        destination = "[$($datastore.Name)] $DestinationPath"
                    }
                }

                Remove-Item -Path $fullDestinationPath -Force
            }

            $destinationDir = Split-Path -Parent $fullDestinationPath
            if (-not (Test-Path $destinationDir)) {
                New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
            }

            Copy-DatastoreItem -Item $FilePath -Destination $fullDestinationPath -Force

            return @{
                changed = $true
                msg = "File uploaded successfully"
                file_name = (Split-Path $FilePath -Leaf)
                destination = "[$($datastore.Name)] $DestinationPath"
            }
        }
        finally {
            Remove-PSDrive -Name $driveName -Force
        }
    }
    catch {
        throw $_
    }
    finally {
        if ($global:DefaultVIServer) {
            Disconnect-VIServer -Server $global:DefaultVIServer -Confirm:$false
        }
        if (-not $ValidateCerts) {
            Set-PowerCLIConfiguration -InvalidCertificateAction Warn -Confirm:$false | Out-Null
        }
    }
}

try {
    $params = @{
        VCenterServer = $module.Params.host
        VCenterUsername = $module.Params.username
        VCenterPassword = $module.Params.password
        DatastoreName = $module.Params.datastore_name
        FilePath = $module.Params.file_path
        DestinationPath = $module.Params.destination_path
        ValidateCerts = $module.Params.validate_certs
    }

    $result = Upload-FileToVCenter @params

    $module.Result.changed = $result.changed
    $module.Result.msg = $result.msg
    $module.Result.file_name = $result.file_name
    $module.Result.destination = $result.destination
}
catch {
    $module.FailJson("Error uploading file: $($_.Exception.Message)", $_)
}

$module.ExitJson()