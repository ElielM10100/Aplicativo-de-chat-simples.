import socket
import threading

def handle_client(client_socket, address, clients):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode("utf-8")
            print(f"Recebido de {address}: {message}")

            # Encaminhar a mensagem para todos os clientes
            for client in clients:
                if client != client_socket:
                    client.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Erro ao lidar com o cliente {address}: {e}")
            break

    print(f"Cliente {address} desconectado.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    host = "127.0.0.1"
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Servidor ouvindo em {host}:{port}")

    clients = []

    while True:
        client_socket, address = server.accept()
        print(f"Nova conexão de {address}")
        clients.append(client_socket)

        client_handler = threading.Thread(target=handle_client, args=(client_socket, address, clients))
        client_handler.start()

if __name__ == "__main__":
    start_server()
