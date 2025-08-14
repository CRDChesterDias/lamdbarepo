import paramiko
import time

# -------------------
# Server A details
# -------------------
server_a = "SERVER_A_IP"
username_a = "USER_A"
password_a = "PASSWORD_A"
sudo_password_a = "SUDO_PASSWORD_A"

# -------------------
# Server B details
# -------------------
server_b = "SERVER_B_IP"
username_b = "USER_B"
password_b = "PASSWORD_B"
script_path = "/path/to/script.sh"

# -------------------
# Connect to Server A
# -------------------
ssh_a = paramiko.SSHClient()
ssh_a.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_a.connect(server_a, username=username_a, password=password_a)

channel = ssh_a.invoke_shell()
time.sleep(1)

# Elevate privileges on Server A (if needed)
channel.send("sudo su -\n")
time.sleep(1)
channel.send(sudo_password_a + "\n")
time.sleep(1)

# SSH into Server B
channel.send(f"ssh {username_b}@{server_b}\n")
time.sleep(2)
channel.send(password_b + "\n")
time.sleep(2)

# Run the script on Server B
channel.send(f"bash {script_path}\n")

# -------------------
# Capture output dynamically
# -------------------
output = ""
while True:
    if channel.recv_ready():
        data = channel.recv(65535).decode()
        output += data
        print(data, end="")  # print live output

    # Check if the script finished by looking for a new prompt
    if output.endswith(f"{username_b}@"):
        break
    time.sleep(1)

# Close connections
channel.close()
ssh_a.close()
