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


locals {
  original_config = {
    cidr_block = "1.1.1.1"
    cross_az = {
      cross_ad  = "2.2.2.2"
      cross_de  = "3.3.3.3"
      cross_dns = "4.4.4.4"
    }
    purpose = "adafd"
  }

  # Convert original_config to the desired new_config structure
    new_config = flatten([
    for entry in local.original_config : [
      for az_key, az_value in entry.cross_az : merge(
        {
          cidr_block = entry.cidr_block
          purpose    = entry.purpose
        },
        {
          cross_az = {
            az_key = az_value
          }
        }
      )
    ]
  ])


}


      for az_key, az_value in entry.cross_az != null ? entry.cross_az : {} : merge(
export AWS_ACCESS_KEY_ID=$(echo $CREDS | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $CREDS | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $CREDS | jq -r '.Credentials.SessionToken')


aws networkmanager describe-global-networks --query "GlobalNetworks[0].CoreNetwork.Arn"
aws ram get-resource-shares --query "resourceShares[0].resourceShareArn"
aws networkmanager describe-global-networks --query "GlobalNetworks[0].CoreNetworkId" --output text

aws s3 cp /path/to/local/file.txt s3://your-bucket-name/your-folder/file.txt


aws networkmanager describe-global-networks
aws networkmanager describe-attachments --global-network-id gn-0123456789abcdef0

