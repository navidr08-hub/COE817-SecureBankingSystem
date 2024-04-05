import socket
import hashlib
import hmac


class Alice:
    def __init__(self):
        self.master_secret = b'YourMasterSecretKey'

    def key_distribution(self):
        """
        Exchange Master Secret key with the server securely.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(("localhost", 45687))
                client_socket.send(b"Initiate Key Distribution")
                self.master_secret = client_socket.recv(1024)
        except ConnectionRefusedError:
            print("Error: Connection to server refused.")

    def perform_transaction(self, action, amount):
        """
        Perform a transaction with the server.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(("localhost", 45687))
                encoded_action = action.encode()
                encoded_amount = amount.encode()
                client_socket.send(encoded_action)
                client_socket.send(encoded_amount)
                client_socket.send(hmac.new(self.master_secret, encoded_action + encoded_amount, hashlib.sha256).digest())
                transaction_result = client_socket.recv(1024).decode()
                print("Transaction Result:", transaction_result)
        except ConnectionRefusedError:
            print("Error: Connection to server refused.")

    def verify_authentication(self, username, password):
            """
            Authenticate the user with the server.
            """
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(("localhost", 45687))
                    client_socket.send(username.encode())
                    client_socket.send(("," + password).encode())
                    return client_socket.recv(1024).decode() == "Authenticated successfully"
            except ConnectionRefusedError:
                print("Error: Connection to server refused.")
                return False


# Example usage:
def main():
    alice = Alice()

    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    is_valid_user = Alice.verify_authentication(username, password)
    if is_valid_user:
        print("User authenticated successfully.")
        alice.key_distribution()
        action = input("Please enter the type of transaction: ")
        amount = input("Please enter the amount: ")
        alice.perform_transaction(action, amount)
    else:
        print("Authentication failed. Invalid username and/or password")


if __name__ == "__main__":
    main()