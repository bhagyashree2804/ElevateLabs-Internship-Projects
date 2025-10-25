# crypto_utils.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64
import hashlib
from datetime import datetime
import json

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, password: str):
    with open(file_path, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)
    iv = os.urandom(12)  # 96-bit IV for GCM

    key = derive_key(password, salt)

    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()

    enc_file_path = os.path.join("encrypted_files", os.path.basename(file_path) + ".enc")
    with open(enc_file_path, 'wb') as f:
        f.write(ciphertext)

    metadata = {
        'original_name': os.path.basename(file_path),
        'time': datetime.now().isoformat(),
        'salt': base64.b64encode(salt).decode(),
        'iv': base64.b64encode(iv).decode(),
        'tag': base64.b64encode(encryptor.tag).decode(),
        'hash': hashlib.sha256(data).hexdigest()
    }
    with open(enc_file_path + '.meta', 'w') as f:
        json.dump(metadata, f)

    print(f"File encrypted and saved as: {enc_file_path}")

def decrypt_file(enc_file_path: str, password: str):
    with open(enc_file_path + '.meta', 'r') as f:
        metadata = json.load(f)

    salt = base64.b64decode(metadata['salt'])
    iv = base64.b64decode(metadata['iv'])
    tag = base64.b64decode(metadata['tag'])
    original_hash = metadata['hash']

    key = derive_key(password, salt)

    with open(enc_file_path, 'rb') as f:
        ciphertext = f.read()

    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    if hashlib.sha256(plaintext).hexdigest() != original_hash:
        raise ValueError("File integrity check failed!")

    decrypted_file_path = os.path.join("decrypted_files", "DEC_" + metadata['original_name'])
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

    print(f"File decrypted and saved as: {decrypted_file_path}")
