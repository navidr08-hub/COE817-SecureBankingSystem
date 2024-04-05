import tkinter as tk
from tkinter import messagebox
import socket


class BankClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")

        # Rest of the BankClientGUI initialization code...
        self.server_address = ("localhost", 8888)

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=0, column=0, padx=(10, 5), pady=5)

        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=0, column=1, padx=5, pady=5)

        self.balance_button = tk.Button(
            master, text="Check Balance", command=self.check_balance
        )
        self.balance_button.grid(row=0, column=2, padx=(5, 10), pady=5)

        self.log_label = tk.Label(master, text="Log:")
        self.log_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.log_text = tk.Text(master, height=5, width=30)
        self.log_text.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

    def send_request(self, action, *args):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(self.server_address)
                client_socket.send(action.encode())
                for arg in args:
                    client_socket.send(arg.encode())
                response = client_socket.recv(1024).decode()
                return response
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def deposit(self):
        amount = self.get_amount()
        if not amount:
            messagebox.showerror("Error", "Please enter amount.")
            return
        response = self.send_request("deposit", amount)
        messagebox.showinfo("Deposit", response)

    def withdraw(self):
        amount = self.get_amount()
        if not amount:
            messagebox.showerror("Error", "Please enter amount.")
            return
        response = self.send_request("withdraw", amount)
        messagebox.showinfo("Withdraw", response)

    def check_balance(self):
        response = self.send_request("balance_inquiry")
        messagebox.showinfo("Balance", f"Balance: ${response}")

    def get_amount(self):
        amount = self.log_text.get("1.0", "end-1c")
        self.log_text.delete("1.0", "end")
        return amount


class LoginForm:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Form")

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        # Perform login validation here
        # If login successful:
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username and password are correct
        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            self.master.destroy()  # Destroy the login form window
            root = tk.Tk()
            app = BankClientGUI(root)  # Display the BankClientGUI
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


def main():
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()


if __name__ == "__main__":
    main()
