from concurrent.futures import thread
from http import client
import os
from pydoc import cli
from socket import SOCK_STREAM, AF_INET, socket
from venv import create
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn
import sys
import signal

from interface.router.stream import router as stream_router
from interface.socket.server import Socket



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

# /streams
app.include_router(stream_router)


@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/favicon.ico", include_in_schema=False)
async def get_favicon():
    return FileResponse('favicon.ico')


# uvicorn.run()은 CTRL+C로 멈추지 않기 때문에
# custom signal handler를 설정해 종료해준다
# CTRL+Z는 uvicorn.run()은 멈추게 할 수는 있지만
# 다른 프로세스들은 멈추게 하지 않는다
def signal_handler(signum, frame):
    sys.exit()


# app이 실행되면
@app.on_event("startup")
async def startup_event():
  

    # custom signal handler 적용
    signal.signal(signal.SIGINT, signal_handler)


def main():
    uvicorn.run("server.app:app", reload=True)
