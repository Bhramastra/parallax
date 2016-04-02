from node import logger
import threading
import socket
import Queue

q=Queue.Queue()

def savefile(q,sock):
    # import pdb
    # pdb.set_trace()
    print "save file thread started"
    try:
        f=open("cloudcode.py","w")
        while 1:
            data=sock.recv(4096)
            print data
            if data:
                f.write(data)
            else:
                f.close()
                break
    except Exception as e:
        print(repr(e))
        q.put((repr(e), threading.current_thread().getName()))


def recvfile(q):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", 1201))
        server_socket.listen(10)
        while 1:
            (clientsocket, address) = server_socket.accept()
            x=threading.Thread(target=savefile, args=(q, clientsocket,), name="Savefile")
            x.setDaemon(True)
            x.start()
    except Exception as e:
        print repr(e)
        q.put((repr(e), threading.current_thread().getName()))


threadlist = [threading.Thread(target=recvfile, args=(q,), name="File Server"),
              threading.Thread(target=logger, args=(q,), name="Logger")]


for t in threadlist:
    t.setDaemon(True)
    t.start()

while 1:
    pass
