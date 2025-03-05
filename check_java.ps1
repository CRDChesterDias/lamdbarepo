# PowerShell script to check running Java processes

# Get all running Java processes
$javaProcesses = Get-Process | Where-Object { $_.ProcessName -like "java*" }

if ($javaProcesses) {
    Write-Output "Java processes are running:"
    $javaProcesses | ForEach-Object {
        Write-Output "Process ID: $($_.Id) - Name: $($_.ProcessName)"
    }
} else {
    Write-Output "No Java processes are running."
}
