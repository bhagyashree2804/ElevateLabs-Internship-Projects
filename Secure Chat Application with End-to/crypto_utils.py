from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

def encrypt_message(message, recipient_public_key_path):
    aes_key = get_random_bytes(32)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())

    with open(recipient_public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return {
        "encrypted_key": base64.b64encode(encrypted_aes_key).decode(),
        "nonce": base64.b64encode(cipher_aes.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

def decrypt_message(encrypted_data, private_key_path):
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    aes_key = private_key.decrypt(
        base64.b64decode(encrypted_data["encrypted_key"]),
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=base64.b64decode(encrypted_data["nonce"]))
    plaintext = cipher_aes.decrypt_and_verify(
        base64.b64decode(encrypted_data["ciphertext"]),
        base64.b64decode(encrypted_data["tag"])
    )

    return plaintext.decode()
