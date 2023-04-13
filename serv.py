import socket
import cv2
import numpy as np
import mss
import threading
import time
import pyautogui


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 5000)) 
server_socket.listen(5) 


def send_screenshot(client_socket):
    while True:
        
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            screenshot = sct.grab(monitor)

           
            screenshot_bytes = cv2.imencode('.png', np.array(screenshot))[1].tobytes()

            
            size_bytes = len(screenshot_bytes).to_bytes(8, byteorder='big')
            client_socket.sendall(size_bytes)

            
            client_socket.sendall(screenshot_bytes)

            
            time.sleep(0.1)

    
    client_socket.close()


def handle_client(client_socket):
    
    send_thread = threading.Thread(target=send_screenshot, args=(client_socket,))
    send_thread.start()

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            data_str = data.decode('utf-8')
            if data_str.startswith('move'):
                parts = data_str.split(' ')
                x, y = map(int, parts[1:])
                pyautogui.moveTo(x, y)

            elif data_str.startswith('click'):
                parts = data_str.split(' ')
                x, y, button = map(int, parts[1:])
                pyautogui.click(x, y, button=button)
        except Exception as e:
            print('Exception while handling client input:', e)

    client_socket.close()


while True:
    
    print('Waiting for client to connect...')
    client_socket, address = server_socket.accept()
    print('Client connected:', address)

    
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
