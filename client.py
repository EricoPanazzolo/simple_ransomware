from socket import *
import os
import threading

server_ip = ""

def create_client_socket():
    try:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        print("Client socket successfully created")
        return client_socket
    except Exception as e:
        print(f"Socket creation failed with error: {e}")
        return None

def send_receive_message(client_socket, server_ip, server_port):
    message = input(f"Input lowercase sentence: ").lower()
    client_socket.sendto(message.encode(), (server_ip, server_port))
    print("Server is sending the messege...")
    modified_message, server_address = client_socket.recvfrom(2048)
    return modified_message.decode()

def start_http_server():
    os.system('python -m http.server 52369 > /dev/null 2>&1 &')

client_socket = create_client_socket()

if client_socket:
    server_port = int(input("Choose the server port: "))
    
    http_server_thread = threading.Thread(target=start_http_server)
    http_server_thread.start()
    
    while True:
        if server_port == 6677:
            modified_message = send_receive_message(client_socket, server_ip, server_port)
            print("server says:", modified_message)
        else:
            modified_message = send_receive_message(client_socket, server_ip, server_port)
            print("server says:", modified_message)
