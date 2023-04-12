import socket
import cv2
import numpy as np
import io
import threading
from tkinter import *
from PIL import Image, ImageTk

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = socket.gethostbyname(socket.gethostname())
server_address = (ip_address, 5000)  # replace with the IP address of the remote computer
client_socket.connect(server_address)

# Create a Tkinter window to display the screenshot
root = Tk()
screenshot_label = Label(root)
screenshot_label.pack()

# Function to receive and display screenshot
def receive_screenshot():
    while True:
        # Receive the size of the byte string from the server
        size_bytes = client_socket.recv(8)

        # Convert the size to an integer
        buffer_size = int.from_bytes(size_bytes, byteorder='big')

        # Receive the byte string from the server
        screenshot_bytes = b''
        while len(screenshot_bytes) < buffer_size:
            remaining = buffer_size - len(screenshot_bytes)
            screenshot_bytes += client_socket.recv(1024 if remaining > 1024 else remaining)

        # Convert the byte string to an image
        screenshot = cv2.imdecode(np.frombuffer(screenshot_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Convert the image to a format that Tkinter can display
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        screenshot = Image.fromarray(screenshot)
        screenshot = ImageTk.PhotoImage(screenshot)

        # Update the screenshot label in the Tkinter window
        screenshot_label.configure(image=screenshot)
        screenshot_label.image = screenshot

    # Close the client socket
    client_socket.close()

# Create a thread to receive and display screenshots from the server
receive_thread = threading.Thread(target=receive_screenshot)
receive_thread.start()

# Start the Tkinter main loop
root.mainloop()
