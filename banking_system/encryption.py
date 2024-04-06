import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

MASTER_SECRET = b''  # Master Secret key shared between ATM and server
AES_KEY = b''  # Key for data encryption
MAC_KEY = b''  # Key for Message Authentication Code


def generate_mac(data):
    """
    Generate a Message Authentication Code (MAC) for data integrity.
    """
    return hmac.new(MAC_KEY, data, hashlib.sha256).digest()


def verify_mac(data, mac_received):
    """
    Verify the Message Authentication Code (MAC) for data integrity.
    """
    return hmac.compare_digest(generate_mac(data), mac_received)


def encrypt(message):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return cipher_text


def decrypt(cipher_text):
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    message = decryptor.update(cipher_text) + decryptor.finalize()
    return message
