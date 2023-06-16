import socket
import struct
import os

def receive_image(client_socket, save_folder):
    # Receive the size of the image
    size_data = client_socket.recv(4)
    image_size = struct.unpack("!I", size_data)[0]

    # Receive the image data
    image_data = b""
    while len(image_data) < image_size:
        data = client_socket.recv(image_size - len(image_data))
        if not data:
            break
        image_data += data

    if len(image_data) == image_size:
        # Get the original image name from the client
        image_name = client_socket.recv(1024).decode()

        # Save the received image
        save_path = os.path.join(save_folder, image_name)
        with open(save_path, "wb") as file:
            file.write(image_data)
        print(f"Image received and saved as {save_path}")
    else:
        print("Incomplete image data received")

def start_server(server_ip, server_port, save_folder):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the server IP and port
        server_socket.bind((server_ip, server_port))
        print(f"Server started on {server_ip}:{server_port}")

        # Listen for incoming connections
        server_socket.listen(1)

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

            # Receive the image from the client
            receive_image(client_socket, save_folder)

            # Close the client connection
            client_socket.close()

    except Exception as e:
        print("Error:", e)
    finally:
        # Close the server socket
        server_socket.close()
        print("Server stopped")


server_ip = "127.0.0.1"  # Listen on all available network interfaces
server_port = 5501
save_folder = "received"
start_server(server_ip, server_port, save_folder)

