import msg
import scheduler
import thread

# Start master server

def start():
    msg.server(1200,type='master')
if __name__ == '__main__':
    thread.start_new_thread(start,())
    thread.start_new_thread(scheduler.run,())

    while 1:
        pass

__author__ = 'gaurav'
