import os
from cryptography.fernet import Fernet

KEY_FILE = "storage/key.key"

def initialize_encryption():
    """Initialize encryption key if it doesn't exist"""
    os.makedirs("storage", exist_ok=True)
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

def load_key():
    """Load encryption key from file"""
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_data(data):
    """Encrypt text data"""
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(data):
    """Decrypt encrypted data"""
    key = load_key()
    f = Fernet(key)
    return f.decrypt(data).decode()