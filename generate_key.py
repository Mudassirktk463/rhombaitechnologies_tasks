# Run this only once to create the key
from cryptography.fernet import Fernet

with open("key.key", "wb") as key_file:
    key_file.write(Fernet.generate_key())
