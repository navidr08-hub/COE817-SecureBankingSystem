from datetime import datetime
import hmac
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Define global variables
MASTER_SECRET = b''  # Master Secret key shared between ATM and server
AES_KEY = b''  # Key for data encryption
MAC_KEY = b''  # Key for Message Authentication Code
AUDIT_LOG_FILE = "../logs/audit_log.txt"

# Dictionary to store account information (username, password, balance)
accounts = {'Alice': {'password': 'password123', 'balance': 1000},
            'Bob': {'password': 'securepwd', 'balance': 500},
            'Eve': {'password': 'password', 'balance': 2000}}


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


def log_transaction(username, action, amount):
    """
    Log the transaction information into an audit log file.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG_FILE, "a") as file:
        file.write(f"Username: {username}, Action: {action}, Amount: {amount}, Time: {now} \n")


def main():
    """ Process request coming from ATM and return decoded data """
    # Given user_id, aes_key, mac_key
    # 1. Receive message from client
    # 2. Use MAC key to apply hash algorithm to message and check if message is authentic
    # 3. If message is authentic, use decryption key (AES) to decrypt the message
    # 4. Split message into request type, and amount
    # 5. Process request and respond with a success msg if successful, otherwise error msg
    # 6. Log request in the audit log while processing the request.

    # Receive message from client
    action = client_socket.recv(1024)
    amount = client_socket.recv(1024)
    mac = client_socket.recv(32)  # 256-bit MAC

    message = action + amount

    # Use MAC key to apply hash algorithm to message and check if message is authentic
    if verify_mac(message, mac):
        # If message is authentic, use decryption key (AES) to decrypt the message
        action = decrypt(action)

        if (action == "quit"):
            pass  # break
        else:
            # Process request and respond with a success msg if successful, otherwise error msg
            # Log request in the audit log while processing the request.
            if (action == "deposit"):
                amount = decrypt(amount)
                accounts[username]['balance'] += amount
                log_transaction(username, action, amount)
            elif (action == "withdraw"):
                amount = decrypt(amount)
                if accounts[username]['balance'] >= amount:
                    accounts[username]['balance'] -= amount
                    log_transaction(username, action, amount)
                else:
                    client_socket.send(b"Insufficient balance")
            elif (action == "balance"):
                balance = str(accounts[username]['balance']).encode()
                # Encrypt and attach MAC then send 
                client_socket.send(balance)
                log_transaction(username, action, amount)
            else:
                pass  # break
            client_socket.send(b"Transaction Successful")
    else:
        client_socket.send(b"Transaction Failed: Integrity Check Failed")
