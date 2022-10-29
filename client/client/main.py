from tabnanny import check
import cv2

# from interface.socket import Socket
import logging
import asyncio
import pickle
import struct
import uuid

# car_id = uuid.uuid4().hex
car_id = "e208d83305274b1daa97e4465cb57c8b"

server_public_ip = input("server ip: ")


def _asyncio():
    async def sending():
        try:
            reader, writer = await asyncio.open_connection(
                host=server_public_ip, port=9999
            )
        except:
            logging.warning("connection failed")
            return
        VC = cv2.VideoCapture(0)
        while True:
            ret, cap = VC.read()
            ret, jpgImg = cv2.imencode(".jpg", cap)
            jpgBin = pickle.dumps(jpgImg)
            writer.write(struct.pack("<L", len(jpgBin)) + jpgBin)
            await writer.drain()

        # writer.close()
        # await writer.wait_closed()
        # VC.release()

    asyncio.run(sending())


if __name__ == "__main__":
    _asyncio()
