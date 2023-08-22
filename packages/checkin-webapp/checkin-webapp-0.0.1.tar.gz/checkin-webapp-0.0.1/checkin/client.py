import socket
import json

def send_message(
        message: str,
        buffer_size_kb: int = 2000,
        server_address = "localhost",
        server_port = 8888
    ) -> str:
    """Send a string message on server_address:server_port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        client_socket.connect((server_address, server_port))
        buffer = buffer_size_kb * 1024

        # Send the message
        client_socket.sendall(message.encode())

        # Receive the response from the server
        response = client_socket.recv(buffer).decode().strip()

        return response


def main():

    response = send_message("Hello Server")
    print(response)



if __name__ == '__main__':
   main()