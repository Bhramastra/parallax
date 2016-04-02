import msg
import scheduler
import threading
from Queue import Queue

q= Queue()


def logger(q):
    print "Logger Thread started"
    try:
        while 1:
            data = q.get()
            print data
    except Exception as e:
        print repr(e)
        return

def start(q,port, type):
    try:
        msg.Server(port,type)
    except Exception as e:
        q.put((repr(e), threading.current_thread().getName()))

if __name__ == '__main__':
    threadlist = [threading.Thread(target=start, args=(q, 1200, "master"), name="Master"),
                  threading.Thread(target=logger, args=(q,), name="Logger")]
    for t in threadlist:
        t.setDaemon(True)
        t.start()

    while 1:
        pass
