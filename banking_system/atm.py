import tkinter as tk
from tkinter import messagebox
import socket

class ATM:
    def __init__(self, master):
        self.master = master
        self.master.title("ATM")

        self.server_address = ("localhost", 8888)

        self.amount_label = tk.Label(master, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=5)
        self.amount_entry = tk.Entry(master)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        self.deposit_button = tk.Button(master, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=1, column=0, padx=10, pady=5)

        self.withdraw_button = tk.Button(master, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=1, column=1, padx=10, pady=5)

        self.balance_button = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.balance_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.log_label = tk.Label(master, text="Log:")
        self.log_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.log_text = tk.Text(master, height=5, width=30)
        self.log_text.grid(row=3, column=1, padx=10, pady=5)

    def send_request(self, action, amount=None):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect(self.server_address)
                # encrypt "action" with AES key
                # encrypt "amount" with AES key
                # concatenate both? then generate mac
                client_socket.send(action.encode())
                if amount is not None:
                    client_socket.send(amount.encode())
                response = client_socket.recv(1024).decode()
                return response
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def deposit(self):
        amount = self.amount_entry.get()
        if not amount:
            messagebox.showerror("Error", "Please enter amount.")
            return
        messagebox.showinfo("Deposit", amount)
        # response = self.send_request("deposit", amount)
        # messagebox.showinfo("Deposit", response)

    def withdraw(self):
        amount = self.amount_entry.get()
        if not amount:
            messagebox.showerror("Error", "Please enter amount.")
            return
        
        messagebox.showinfo("Withdraw", amount)
        # response = self.send_request("withdraw", amount)
        # messagebox.showinfo("Withdraw", response)

    def check_balance(self):
        # response = self.send_request("balance_inquiry")
        messagebox.showinfo("Balance", "something")
        # messagebox.showinfo("Balance", f"Balance: ${response}")

def main():
    root = tk.Tk()
    app = ATM(root)
    root.mainloop()

if __name__ == "__main__":
    main()
