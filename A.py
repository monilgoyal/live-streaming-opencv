import socket
import threading
import cv2
import numpy
from io import BytesIO

######### server A #######
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1",2323))
server.listen()

ip=input('Enter Friend\'s IP: ')
port=int(input('Enter Friend\'s Port Number: '))

####### client for B #########
remoteserver=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remoteserver.connect((ip,port))

###### receiving data from client B #######
def receive():
    client,address=server.accept()      #### accept connections ####
    while True:
        np_bytes = client.recv(1000000) #### 10lac bytes data received ####
        if not np_bytes:
            break
        load_bytes = BytesIO(np_bytes)
        try:
            photo_recv = numpy.load(load_bytes)
        except:
            pass
        cv2.imshow("ClientB", photo_recv)
        cv2.waitKey(1)
        if cv2.waitKey(10)==13:
            break
    cv2.destroyAllWindows()
    client.close()

######## sending data to server B #######
def send():
    cap=cv2.VideoCapture(0)
    while True:
        try:
            ret,photo=cap.read()
            np_bytes = BytesIO()
            numpy.save(np_bytes, photo)
            np_bytes = np_bytes.getvalue()
            remoteserver.send(np_bytes)
        except:
            cap.release()
            break 

######## Creating Threads #######
T1=threading.Thread(target=send)
T2=threading.Thread(target=receive)

######## Starting Threads #######
T1.start()
T2.start()