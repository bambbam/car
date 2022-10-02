import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from interface.socket.server import get_socket

router = APIRouter(prefix="/streams", tags=["streams"])

async def read_video():
    socket = get_socket()
    try:
        with socket.connect() as connection:
            while(True):
                length = connection.recv(4)
                length = int.from_bytes(length, byteorder='little')
                logging.info(f"length: {length}")
                yield connection.recv(length)
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="server is not watching")
    

@router.get("/")
async def read_all_videos():
    return StreamingResponse(read_video(), media_type="multipart/x-mixed-replace; boundary=PNPframe")

