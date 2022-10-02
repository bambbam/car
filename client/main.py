import cv2
from interface.socket import Socket
import logging


def main(): 
    check_socket = True
    try:
        socket_client = Socket(
            host="127.0.0.1",
            port=9999
        )
    except:
        logging.warn("server is not watching")
        check_socket = False
    while(True):
        try:
            ret, cap = cv2.VideoCapture(0).read()     
            ret, jpgImg = cv2.imencode(".jpg", cap)                                 
            jpgBin = bytearray(jpgImg.tobytes())
            if check_socket:
                l = len(b'--PNPframe\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpgBin + b'\r\n')
                socket_client.send(l.to_bytes(4, byteorder='little'))
                socket_client.send(b'--PNPframe\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpgBin + b'\r\n')
            cv2.imshow("Client", cap)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            socket_client = Socket(
                host="127.0.0.1",
                port=9999
            )

    socket_client.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
