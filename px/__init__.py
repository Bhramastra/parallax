import socket


def execute(function,args,max_nodes=10):
    print "this is execute function"


def deploy(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(('0.0.0.0', 1201))
        f = open(filename, "rb")
        try:
            bytes_read = f.read(1)
            print bytes_read
            print "after bytes"
            while bytes_read:
                s.send(bytes_read)
                bytes_read = f.read(1)
            return 0
        except Exception as e:
            print str(e)
            return -1
        finally:
            s.send("$exit")
            f.close()
            s.close()
    except Exception as e:
        print str(e)
        return -1

__author__ = 'gaurav'
