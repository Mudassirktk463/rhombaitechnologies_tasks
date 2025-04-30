import socket
from cryptography.fernet import Fernet
import getpass

# Load encryption key
with open("key.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Connect to server
client = socket.socket()
client.connect(('localhost', 9999))

# Send credentials
username = input("Username: ")
password = getpass.getpass("Password: ")
client.send(username.encode())
client.send(password.encode())

status = client.recv(1024)
if status != b"AUTH_SUCCESS":
    print("❌ Authentication Failed.")
    client.close()
    exit()

# Choose file to send
file_name = input("Enter file name to send: ")
with open(file_name, "rb") as f:
    data = f.read()

encrypted = fernet.encrypt(data)

# Send file
client.send(file_name.encode())
client.send(encrypted)

print("File sent successfully.")

client.close()
