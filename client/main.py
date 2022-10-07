from tabnanny import check
import cv2
from interface.socket import Socket
import logging
import asyncio
import pickle
import struct

def _asyncio():
    async def sending():
        try:
            reader, writer = await asyncio.open_connection(host='127.0.0.1', port=9999)
        except:
            logging.warning("connection failed")
            return
        VC = cv2.VideoCapture(0)
        VC.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        VC.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        VC.set(cv2.CAP_PROP_FPS, 12)
        while True:
            ret, cap = VC.read()
            ret, jpgImg = cv2.imencode(".jpg", cap)
            jpgBin = pickle.dumps(jpgImg)
            try:
                writer.write(
                    struct.pack("<L", len(jpgBin)) +
                    jpgBin
                )
                await writer.drain()
            except:
                print('Server down! Wait until the server wake up')
                break
            #cv2.imshow("Client", cap)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
            
        writer.close()
        await writer.wait_closed()
        VC.release()
        #cv2.destroyAllWindows()

    asyncio.run(sending())


if __name__ == "__main__":
    _asyncio()