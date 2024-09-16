Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
mkdir -p /tmp/logs
touch /tmp/logs/hostname.txt
touch /tmp/logs/arc.txt
touch /tmp/logs/nesus.txt
touch /tmp/logs/cloudwatch.txt
hostname=$(cat /tmp/logs/hostname.txt| grep "updated")
if [[ "$hostname" == "" ]]; then 
 sudo /bin/echo "testhost" > /etc/hostname
 sudo hostnamectl set-hostname testhost
 mkdir /tmp/logs
 /bin/echo "updated" > /tmp/logs/hostname.txt
 sudo reboot
else
 arc=$(cat /tmp/logs/arc.txt| grep "updated")
 nesus=$(cat /tmp/logs/nesus.txt| grep "updated")
 cloudwatch=$(cat /tmp/logs/cloudwatch.txt| grep "updated")
 if [[ "$arc" == "" ]]; then
 sudo yum install -y wget
 /bin/echo "updated" > /tmp/logs/arc.txt
 fi
 if [[ "$nesus" == "" ]]; then
 /bin/echo "updated" > /tmp/logs/nesus.txt
 fi
 if [[ "$cloudwatch" == "" ]]; then
 /bin/echo "updated" > /tmp/logs/cloudwatch.txt
 fi
fi 
--//
