<powershell>
$agentInstallerUrl = "https://amazoncloudwatch-agent.s3.amazonaws.com/windows/amd64/latest/amazon-cloudwatch-agent.msi"
$agentServiceName = "AmazonCloudWatchAgent"

# Download the CloudWatch Agent installers
Write-Output "Downloading CloudWatch Agent installer..."
Invoke-WebRequest -Uri $agentInstallerUrl -OutFile 'C:\amazon-cloudwatch-agent.msi'

Write-Output "CloudWatch Agent installation..."
Start-Process msiexec.exe -ArgumentList "/i `"C:\amazon-cloudwatch-agent.msi`"" -Wait -NoNewWindow
Write-Output "CloudWatch Agent installed..."
& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a start -m ec2 -s
</powershell>
