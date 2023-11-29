import paramiko

# Thong tin ket noi SSH
hostname = '192.168.0.206'
port = 22
username = 'root'
password = '123456a@B'

# Tao doi tuong SSHClient
client = paramiko.SSHClient()

# Thiet lap chinh sach mac dinh de chap nhan khoa host ma khong can xac nhan
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Ket noi SSH
    client.connect(hostname, port, username, password)

    # Thuc hien lenh poweroff
    stdin, stdout, stderr = client.exec_command('poweroff')

    # Doc va in ra output va error (neu co)
    print(stdout.read().decode())
    print(stderr.read().decode())

finally:
    # Dong ket noi khi hoan thanh
    client.close()
