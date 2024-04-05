import tkinter as tk
from tkinter import messagebox
import socket

class BankClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")

        self.server_address = ('localhost', 8888)

        self.username_label = tk.Label(master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=2, column=0, padx=10, pady=5)

        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=2, column=1, padx=10, pady=5)

        self.balance_button = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.balance_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.log_label = tk.Label(master, text="Log:")
        self.log_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.log_text = tk.Text(master, height=5, width=30)
        self.log_text.grid(row=4, column=1, padx=10, pady=5)

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
        username = self.username_entry.get()
        amount = self.password_entry.get()
        if not username or not amount:
            messagebox.showerror("Error", "Please enter both username and amount.")
            return
        response = self.send_request("deposit", username, amount)
        messagebox.showinfo("Deposit", response)

    def withdraw(self):
        username = self.username_entry.get()
        amount = self.password_entry.get()
        if not username or not amount:
            messagebox.showerror("Error", "Please enter both username and amount.")
            return
        response = self.send_request("withdraw", username, amount)
        messagebox.showinfo("Withdraw", response)

    def check_balance(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter username.")
            return
        response = self.send_request("balance_inquiry", username)
        messagebox.showinfo("Balance", f"Balance for {username}: ${response}")

def main():
    root = tk.Tk()
    app = BankClientGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()