from concurrent.futures import thread
from http import client
import os
from pydoc import cli
from socket import SOCK_STREAM
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import threading
import struct
import pickle

from interface.router.stream import router as stream_router
from interface.router.stream import get_socket
from interface.socket.server import Socket

db = []

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stream_router)

@app.get('/')
async def root():
    return {
        "message": "hello"
    }

def getCameraStream():
    while True:
        yield (b'--PNPframe\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(db[-1]) + b'\r\n')

@app.get('/stream')
async def stream():
    return StreamingResponse(getCameraStream(), media_type="multipart/x-mixed-replace; boundary=PNPframe")


class ReceiveCapFromClient(threading.Thread):
    def __init__(self, db):
        threading.Thread.__init__(self)
        self.db = db
        self.socket = Socket("127.0.0.1", 9999)
        self.buffer = b''
        self.len_size = struct.calcsize("<L")


    def run(self):
        while True:
            with self.socket.connect() as client_socket:
                while True:
                    flag = 0
                    while len(self.buffer) < self.len_size:
                        recved = client_socket.recv(4096)
                        if not recved:
                            flag = 1
                            break
                        self.buffer += recved

                    if flag:
                        break

                    packed_jpgBin_size = self.buffer[:self.len_size]
                    self.buffer = self.buffer[self.len_size:]

                    jpgBin_size = struct.unpack("<L", packed_jpgBin_size)[0]

                    while len(self.buffer) < jpgBin_size:
                        recved = client_socket.recv(4096)
                        if not recved:
                            break
                        self.buffer += recved
                    
                    jpgBin = self.buffer[:jpgBin_size]
                    self.buffer = self.buffer[jpgBin_size:]

                    jpgImg = pickle.loads(jpgBin)
                    cap = cv2.imdecode(jpgImg, cv2.IMREAD_UNCHANGED)
                    #b, g, r = cv2.split(cap)
                    #cap = cv2.merge([r, g, b])
                    db.append(jpgImg.tobytes())



@app.on_event("startup")
async def startup_event():
    f = ReceiveCapFromClient(db)
    f.start()