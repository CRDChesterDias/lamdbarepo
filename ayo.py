#!/usr/bin/env python3

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import csv

def get_all_hosts(content):
    """Return a list of all ESXi hosts"""
    container = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    return container.view

def main():
    # vCenter connection details
    vcenter_ip = "your-vcenter-ip-or-host"
    vcenter_user = "your-username"
    vcenter_pwd = "your-password"

    # CSV file to store results
    csv_file = "vm_startup_report.csv"

    # Ignore SSL for self-signed certificates
    context = ssl._create_unverified_context()

    # Connect to vCenter
    si = SmartConnect(host=vcenter_ip, user=vcenter_user, pwd=vcenter_pwd, sslContext=context)
    content = si.RetrieveContent()

    # Open CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Host", "VM Name", "Startup Type"])

        hosts = get_all_hosts(content)

        for host in hosts:
            auto_start_manager = host.configManager.autoStartManager

            if not auto_start_manager or not auto_start_manager.config:
                continue

            power_info_list = auto_start_manager.config.powerInfo
            if not power_info_list:
                continue

            for vm_info in power_info_list:
                vm_ref = vm_info.key
                vm_name = vm_ref.name if vm_ref else "Unknown VM"

                # Determine startup type
                start_action = vm_info.startAction
                if start_action == "powerOn":
                    startup_type = "Automatic"
                else:
                    startup_type = "Manual"

                # Write row to CSV
                writer.writerow([host.name, vm_name, startup_type])

    print(f"VM startup report saved to {csv_file}")
    Disconnect(si)

if __name__ == "__main__":
    main()
