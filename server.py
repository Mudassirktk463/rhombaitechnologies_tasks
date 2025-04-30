import socket
import os
from cryptography.fernet import Fernet
from auth import authenticate
from datetime import datetime

# Load encryption key
with open("key.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Create server socket
server = socket.socket()
server.bind(('0.0.0.0', 9999))
server.listen(1)
print("[+] Server is listening on port 9999...")

conn, addr = server.accept()
print(f"[+] Connected by {addr}")

# Authenticate user
username = conn.recv(1024).decode()
password = conn.recv(1024).decode()

if not authenticate(username, password):
    conn.send(b"AUTH_FAIL")
    conn.close()
    exit()

conn.send(b"AUTH_SUCCESS")

# Receive encrypted file
file_name = conn.recv(1024).decode()
file_data = conn.recv(100000)
decrypted = fernet.decrypt(file_data)

# Save file
with open(f"received_{file_name}", "wb") as f:
    f.write(decrypted)

# Log transfer
with open("audit.log", "a") as log:
    log.write(f"[{datetime.now()}] Received file: {file_name} from {username}\n")

print(f"[+] File {file_name} received and decrypted.")

conn.close()
