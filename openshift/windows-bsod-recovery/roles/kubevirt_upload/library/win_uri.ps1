#!powershell

# Copyright: (c) 2015, Corwin Brown <corwin@corwinbrown.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#Requires -Module Ansible.ModuleUtils.Legacy

$params = Parse-Args $args -supports_check_mode $true
$check_mode = Get-AnsibleParam -obj $params -name "_ansible_check_mode" -type "bool" -default $false

$url = Get-AnsibleParam -obj $params -name "url" -type "str" -failifempty $true
$method = Get-AnsibleParam -obj $params -name "method" -type "str" -default "GET" -validateset "CONNECT","DELETE","GET","HEAD","MERGE","OPTIONS","PATCH","POST","PUT","REFRESH","TRACE"
$content_type = Get-AnsibleParam -obj $params -name "content_type" -type "str"
$body = Get-AnsibleParam -obj $params -name "body" -type "str"
$src = Get-AnsibleParam -obj $params -name "src" -type "path"
$remote_src = Get-AnsibleParam -obj $params -name "remote_src" -type "bool" -default $false
$dest = Get-AnsibleParam -obj $params -name "dest" -type "path"
$headers = Get-AnsibleParam -obj $params -name "headers" -type "dict" -default @{}
$maximum_redirection = Get-AnsibleParam -obj $params -name "maximum_redirection" -type "int" -default 5
$return_content = Get-AnsibleParam -obj $params -name "return_content" -type "bool" -default $false
$status_code = Get-AnsibleParam -obj $params -name "status_code" -type "list" -default @(200)
$timeout = Get-AnsibleParam -obj $params -name "timeout" -type "int" -default 30
$validate_certs = Get-AnsibleParam -obj $params -name "validate_certs" -type "bool" -default $true
$url_username = Get-AnsibleParam -obj $params -name "url_username" -type "str" -aliases "user","username"
$url_password = Get-AnsibleParam -obj $params -name "url_password" -type "str" -aliases "password" -no_log $true
$force_basic_auth = Get-AnsibleParam -obj $params -name "force_basic_auth" -type "bool" -default $false
$use_default_credentials = Get-AnsibleParam -obj $params -name "use_default_credentials" -type "bool" -default $false
$client_cert = Get-AnsibleParam -obj $params -name "client_cert" -type "path"
$client_cert_password = Get-AnsibleParam -obj $params -name "client_cert_password" -type "str" -no_log $true
$creates = Get-AnsibleParam -obj $params -name "creates" -type "path"
$removes = Get-AnsibleParam -obj $params -name "removes" -type "path"

$result = @{
    changed = $false
    url = $url
}

Function Get-FileStream {
    param (
        [string]$FilePath,
        [bool]$RemoteSrc
    )

    if ($RemoteSrc) {
        if (Test-Path $FilePath) {
            return [System.IO.File]::OpenRead($FilePath)
        }
        else {
            Fail-Json -obj $result -message "File not found: $FilePath"
        }
    }
    else {
        $bytes = [System.Convert]::FromBase64String($FilePath)
        $memoryStream = New-Object System.IO.MemoryStream
        $memoryStream.Write($bytes, 0, $bytes.Length)
        $memoryStream.Seek(0, [System.IO.SeekOrigin]::Begin)
        return $memoryStream
    }
}

if ($creates -and (Test-Path -LiteralPath $creates)) {
    $result.skipped = $true
    $result.msg = "The 'creates' file or directory ($creates) already exists."
    Exit-Json -obj $result
}

if ($removes -and -not (Test-Path -LiteralPath $removes)) {
    $result.skipped = $true
    $result.msg = "The 'removes' file or directory ($removes) does not exist."
    Exit-Json -obj $result
}

# Create the request object
$request = [System.Net.WebRequest]::Create($url)
$request.Method = $method
$request.Timeout = $timeout * 1000
$request.AllowAutoRedirect = $false
$request.MaximumAutomaticRedirections = $maximum_redirection

if (-not $validate_certs) {
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
}

if ($null -ne $content_type) {
    $request.ContentType = $content_type
}

foreach ($header in $headers.GetEnumerator()) {
    $request.Headers.Add($header.Name, $header.Value)
}

if ($use_default_credentials) {
    $request.UseDefaultCredentials = $true
}

if ($client_cert) {
    if (-not (Test-Path -LiteralPath $client_cert)) {
        Fail-Json -obj $result -message "Client certificate '$client_cert' does not exist"
    }
    try {
        $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($client_cert, $client_cert_password)
        $request.ClientCertificates.Add($cert) | Out-Null
    }
    catch {
        Fail-Json -obj $result -message "Failed to read client certificate '$client_cert': $($_.Exception.Message)"
    }
}

if ($null -ne $url_username) {
    if ($force_basic_auth) {
        $basic_value = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes("$($url_username):$($url_password)"))
        $request.Headers.Add("Authorization", "Basic $basic_value")
    }
    else {
        $sec_password = ConvertTo-SecureString -String $url_password -AsPlainText -Force
        $credential = New-Object System.Management.Automation.PSCredential($url_username, $sec_password)
        $request.Credentials = $credential
    }
}

try {
    if ($src) {
        $fileStream = Get-FileStream -FilePath $src -RemoteSrc $remote_src
        $request.ContentLength = $fileStream.Length
        $requestStream = $request.GetRequestStream()
        $fileStream.CopyTo($requestStream)
        $requestStream.Close()
        $fileStream.Close()
    }
    elseif ($body) {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
        $request.ContentLength = $bytes.Length
        $requestStream = $request.GetRequestStream()
        $requestStream.Write($bytes, 0, $bytes.Length)
        $requestStream.Close()
    }

    $response = $request.GetResponse()
    $result.status_code = [int]$response.StatusCode

    if ($return_content) {
        $responseStream = $response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($responseStream)
        $result.content = $reader.ReadToEnd()
        $reader.Close()
        $responseStream.Close()

        if ($dest) {
            if (-not $check_mode) {
                [System.IO.File]::WriteAllText($dest, $result.content)
            }
            $result.dest = $dest
        }
    }

    $result.changed = $true
    $result.msg = "HTTP request successful"

    if ($status_code -notcontains $result.status_code) {
        Fail-Json -obj $result -message "Status code of '$($result.status_code)' was not in the expected status code list: $status_code"
    }
}
catch [System.Net.WebException] {
    $result.status_code = [int]$_.Exception.Response.StatusCode
    $result.msg = $_.Exception.Message
    Fail-Json -obj $result -message "Error calling web request: $($_.Exception.Message)"
}
finally {
    if ($null -ne $response) {
        $response.Close()
    }
}

Exit-Json -obj $result