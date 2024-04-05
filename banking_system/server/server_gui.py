import tkinter as tk
from tkinter import scrolledtext


class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Server")
        self.root.geometry("400x300")

        self.log_text = scrolledtext.ScrolledText(self.root, width=40, height=15)
        self.log_text.pack(pady=10)

        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_button.pack()

    def start_server(self):
        # Add server startup logic here
        self.log_text.insert(tk.END, "Server started...\n")


def main():
    root = tk.Tk()
    server_gui = ServerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()