import paramiko

# Define the SSH connection parameters
hostname = '10.210.102.209'
username = 'admin'
password = 'busan'  # Update with your actual password

# Create an SSH client instance
ssh_client = paramiko.SSHClient()

# Automatically add the server's host key
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the device
ssh_client.connect(hostname, username=username, password=password)

# Create an interactive shell session
ssh_shell = ssh_client.invoke_shell()

# Send the command to show the running configuration
ssh_shell.send('terminal length 0\n')  # Set terminal length to 0 to get the full output
ssh_shell.send('show running-config\n')

# Wait for the command to complete
while not ssh_shell.recv_ready():
    pass

# Receive and decode the output
output = ssh_shell.recv(65535).decode('utf-8')

# Save the output to a file
with open('config.txt', 'w') as file:
    file.write(output)

# Close the SSH session
ssh_client.close()

print('Running configuration saved to config.txt')
