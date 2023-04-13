import socket
import cv2
import numpy as np
import io
import threading
from tkinter import *
from PIL import Image, ImageTk


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address ="192.168.56.1"
server_address = (ip_address, 5000)  
client_socket.connect(server_address)


root = Tk()
screenshot_label = Label(root)
screenshot_label.pack()

# create a small window to track mouse movements and clicks
mouse_window = Toplevel()
mouse_window.geometry('50x50')
mouse_window.protocol("WM_DELETE_WINDOW", lambda: None) # disable closing the window

# track mouse movements and send them to the server
def send_mouse_position(event):
    x, y = event.x, event.y
    mouse_position = f'mouse_position:{x},{y}'
    client_socket.sendall(mouse_position.encode())

# track mouse clicks and send them to the server
def send_mouse_click(event):
    x, y = event.x, event.y
    mouse_click = f'mouse_click:{x},{y},{event.num}'
    client_socket.sendall(mouse_click.encode())

# attach the mouse movement and click handlers to the mouse window
mouse_window.bind('<Motion>', send_mouse_position)
mouse_window.bind('<Button>', send_mouse_click)


def receive_screenshot():
    while True:
        
        size_bytes = client_socket.recv(8)

        
        buffer_size = int.from_bytes(size_bytes, byteorder='big')

       
        screenshot_bytes = b''
        while len(screenshot_bytes) < buffer_size:
            remaining = buffer_size - len(screenshot_bytes)
            screenshot_bytes += client_socket.recv(1024 if remaining > 1024 else remaining)

        
        screenshot = cv2.imdecode(np.frombuffer(screenshot_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

        
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        screenshot = Image.fromarray(screenshot)
        screenshot = ImageTk.PhotoImage(screenshot)

        
        screenshot_label.configure(image=screenshot)
        screenshot_label.image = screenshot

   
    client_socket.close()


receive_thread = threading.Thread(target=receive_screenshot)
receive_thread.start()


root.mainloop()
