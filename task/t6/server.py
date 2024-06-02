import socket
import threading


def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} established.")

    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"Client: {message}")
                broadcast(message, client_socket)
            else:
                print(f"Connection from {client_address} closed.")
                client_socket.close()
                break
        except:
            print(f"An error occurred with {client_address}.")
            client_socket.close()
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                print("An error occurred while broadcasting message.")

def send_messages():
    while True:
        message = input("Server: ")
        broadcast("Server: " + message, None)


def main():
    host = '127.0.0.1'  
    port = 5555  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))


    server_socket.listen()

    print(f"Server listening on {host}:{port}")


    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

    while True:

        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)


        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

clients = []

if __name__ == "__main__":
    main()
