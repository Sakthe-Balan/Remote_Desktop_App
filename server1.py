import socket
import cv2
import numpy as np
import mss
import threading
import time

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 5000)) # Listen on all available network interfaces
server_socket.listen(5) # Allow up to 5 clients to connect simultaneously

# Function to send screenshots to the client
def send_screenshot(client_socket):
    while True:
        # Take a screenshot
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            screenshot = sct.grab(monitor)

            # Convert the screenshot to a byte string
            screenshot_bytes = cv2.imencode('.png', np.array(screenshot))[1].tobytes()

            # Send the size of the byte string to the client
            size_bytes = len(screenshot_bytes).to_bytes(8, byteorder='big')
            client_socket.sendall(size_bytes)

            # Send the byte string to the client
            client_socket.sendall(screenshot_bytes)

            # Wait for 0.1 seconds before taking the next screenshot
            time.sleep(0.1)

    # Close the client socket
    client_socket.close()

# Function to handle client connections
def handle_client(client_socket):
    # Create a thread to send screenshots to the client
    send_thread = threading.Thread(target=send_screenshot, args=(client_socket,))
    send_thread.start()

# Main loop to accept client connections
while True:
    # Wait for a client to connect
    print('Waiting for client to connect...')
    client_socket, address = server_socket.accept()
    print('Client connected:', address)

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
