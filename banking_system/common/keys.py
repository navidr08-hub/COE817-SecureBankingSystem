import hashlib

def generate_master_secret():
    # Generate master secret using a secure hash function
    return hashlib.sha256(shared_key).digest()

def generate_keys(master_secret):
    # Derive encryption key and MAC key from master secret
    encryption_key = master_secret[:16]  # 128 bits for AES encryption
    mac_key = master_secret[16:]         # Remaining for MAC
    return encryption_key, mac_key