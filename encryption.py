import os
from cryptography.fernet import Fernet

KEY_FILE = "storage/key.key"

# Initialize encryption key
def initialize_encryption():
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

# Load key from file
def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

# Encrypt text data
def encrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

# Decrypt encrypted data
def decrypt_data(data):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(data).decode()
