<powershell>
$newHostname = "testhost"
$currentHostname = (Get-WmiObject Win32_ComputerSystem).Name
if ($currentHostname -ne $newHostname) {
  Rename-Computer -NewName $newHostname -Force
  Restart-Computer -Force
}
else {
  $hostnamesFile = "C:\AgentLogs.txt"
  $currentHostname = (Get-WmiObject Win32_ComputerSystem).Name
  Get-Content $hostnamesFile | Out-File -FilePath $hostnamesFile -Encoding UTF8
  Add-Content -Path $hostnamesFile -Value $currentHostname
  $fileContent = Get-Content $hostnamesFile -Raw
  if ($fileContent -notlike "*ARC*") {
    $hostnamesFile = "C:\AgentLogs.txt"
    Add-Content -Path $hostnamesFile -Value 'ARC installed'
  }
  if ($fileContent -notlike "*NESUS*") {
    $hostnamesFile = "C:\AgentLogs.txt"
    Add-Content -Path $hostnamesFile -Value 'NESUS installed'
  }
  if ($fileContent -notlike "*CloudWatch*") {
    $agentInstallerUrl = "https://amazoncloudwatch-agent.s3.amazonaws.com/windows/amd64/latest/amazon-cloudwatch-agent.msi"
    $agentServiceName = "AmazonCloudWatchAgent"

    # Download the CloudWatch Agent installers
    Write-Output "Downloading CloudWatch Agent installer..."
    Invoke-WebRequest -Uri $agentInstallerUrl -OutFile 'C:\amazon-cloudwatch-agent.msi'

    Write-Output "CloudWatch Agent installation..."
    Start-Process msiexec.exe -ArgumentList "/i `"C:\amazon-cloudwatch-agent.msi`"" -Wait -NoNewWindow
    Write-Output "CloudWatch Agent installed..."
    & "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a start -m ec2 -s
    $hostnamesFile = "C:\AgentLogs.txt"
    Add-Content -Path $hostnamesFile -Value 'CloudWatch installed'
  }
 }
</powershell>
<persist>true</persist>
