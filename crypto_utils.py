from cryptography.fernet import Fernet
import hashlib
import base64

def generate_aes_key(shared_secret):
    return base64.urlsafe_b64encode(
        hashlib.sha256(str(shared_secret).encode()).digest()
    )

def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data)

def decrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.decrypt(data)
