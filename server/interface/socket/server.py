## socket server
import socket

from cv2 import INTER_AREA

from base.singleton import Singleton


class Socket(Singleton):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        # self.connection, self.address = self.socket.accept()

    def connect(self):
        return Connection(self.socket)

    def close(self):
        self.socket.close()


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __enter__(self):
        self.connection, self.address = self.socket.accept()
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()


def get_socket():
    socket = Socket("127.0.0.1", 9999)
    return socket
