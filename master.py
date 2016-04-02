import msg
import scheduler
import thread

# Start master server
def start(port, type):
    server = msg.Server(port,type)

if __name__ == '__main__':
    thread.start_new_thread(start,(1200,'master'))
    # thread.start_new_thread(start,(1201,'fileshare'))
    thread.start_new_thread(start,(1202,'scheduler'))
    # thread.start_new_thread(scheduler.run,())

    while 1:
        pass

__author__ = 'gaurav'
