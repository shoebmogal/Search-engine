import socket
import sys

HOST = 'localhost'    # The remote host
PORT = 50017              # The same port as used by the server


while True:
    print("Enter command :>")
    
    cmd = input(">")
    print("Read cmd")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    #s.sendall(b'crawl test.txt')
    s.sendall(cmd.encode("utf-8"))
    data = s.recv(1024)
    s.close()
print('Received', repr(data))
