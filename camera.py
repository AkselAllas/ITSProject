import socket
import cv2
import numpy as np
import time

TARGET_IP = "192.168.1.1"
PORT = 5555

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET_IP, PORT))
    print("[+] Socket initialized")
    return s

def listen(sock):
    print("[+] Waiting for packets")
    while 1:
        data = sock.recv(8192)
        nparr = np.fromstring(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('frame', frame)
        time.sleep(2)
    conn.close()

s = setupSocket()
listen(s)