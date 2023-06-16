import socket
import struct
import os

def send_image(image_path, server_ip, server_port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print("Connected to the server")

        # Read the image file as binary data
        with open(image_path, "rb") as file:
            image_data = file.read()

        # Send the size of the image
        size_data = struct.pack("!I", len(image_data))
        client_socket.sendall(size_data)

        # Send the image data to the server
        client_socket.sendall(image_data)

        # Send the image name to the server
        image_name = os.path.basename(image_path)
        client_socket.send(image_name.encode())

        print("Image sent successfully")

    except Exception as e:
        print("Error:", e)
    finally:
        # Close the socket connection
        client_socket.close()
        print("Connection closed")

# Send images from a folder to the server
folder_contents = os.listdir("detected")
while True:
    for item in folder_contents:
        if item.lower().endswith((".jpg", ".jpeg")):
            image_path = os.path.join("detected", item)
            server_ip = "127.0.0.1"
            server_port = 5501
            send_image(image_path,server_ip,server_port)

