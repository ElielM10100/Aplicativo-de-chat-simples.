import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

class ChatClientGUI:
    def __init__(self, root, username, server_address, server_port):
        self.root = root
        self.root.title("Chat - " + username)

        self.username = username
        self.server_address = server_address
        self.server_port = server_port

        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=15)
        self.chat_history.pack(padx=10, pady=10)

        self.message_entry = Entry(root, width=40)
        self.message_entry.pack(pady=5)

        self.send_button = Button(root, text="Enviar", command=self.send_message)
        self.send_button.pack(pady=5)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_address, self.server_port))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send((self.username + ": " + message).encode("utf-8"))
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                message = data.decode("utf-8")
                self.chat_history.insert(tk.END, message + "\n")
                self.chat_history.yview(tk.END)
            except Exception as e:
                print(f"Erro ao receber mensagens: {e}")
                break

if __name__ == "__main__":
    username = input("Digite seu nome de usuário: ")
    server_address = input("Digite o endereço do servidor: ")
    server_port = int(input("Digite a porta do servidor: "))

    root = tk.Tk()
    chat_client = ChatClientGUI(root, username, server_address, server_port)
    root.mainloop()
