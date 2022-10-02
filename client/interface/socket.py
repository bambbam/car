import socket

class Socket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, length = 1024):
        return self.socket.recv(length)

    def close(self):
        self.socket.close()