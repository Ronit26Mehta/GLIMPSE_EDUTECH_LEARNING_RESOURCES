import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print("\n" + message)
        except:
            print("An error occurred!")
            client_socket.close()
            break
def send_messages(client_socket):
    while True:
        message = input("Client: ")
        client_socket.send(message.encode("utf-8"))

# Main function
def main():
    host = '127.0.0.1'  
    port = 5555  


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    client_socket.connect((host, port))


    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

    send_thread.join()
    receive_thread.join()

if __name__ == "__main__":
    main()
