Param
(
    [Parameter(Mandatory=$true)]
    [string]$ServiceState
)
# Sample parameterized script for use with powershell_script.yml
Get-Service | Where-Object -FilterScript {$_.Status -eq $ServiceState} | Select-Object -Property 'Name'
