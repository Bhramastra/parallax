import socket
import thread
def recv_thread():
    s=socket.socket()
    s.connect(('0.0.0.0',1200))
    s.send("node")
    while 1:
        data=s.recv(1024)
        print data

def send_thread():
    s=socket.socket()
    s.connect(('0.0.0.0',1200))
    s.send("node")
    while 1:
        s.send("hey")


thread.start_new_thread()
__author__ = 'gaurav'
