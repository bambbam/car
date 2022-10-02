import os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from interface.router.stream import router as stream_router
from interface.router.stream import get_socket
from interface.socket.server import Socket

app = FastAPI()
socket = Socket("127.0.0.1", 9999)

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
