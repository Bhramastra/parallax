import sys
import socket
import select



class FileServer:
    NODE_LIST = []
    HOST = '0.0.0.0'
    RECV_BUFFER = 4096
    port= 1201
    type= 'fileshare'

    def __init__(self, port, type):
        self.port=port
        self.type=type
        self.RECV_BUFFER=4096
        self.server()

    def server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.HOST, self.port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        self.NODE_LIST.append(server_socket)

        print "%s server started on port %s" % (self.type, str(self.port))

        while 1:
            ready_to_read,ready_to_write,in_error = select.select(self.NODE_LIST,[],[],0)
            for sock in ready_to_read:
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    type=sockfd.recv(4)
                    print type
                    if type == "node":
                        self.NODE_LIST.append(sockfd)
                        print self.NODE_LIST
                    if type == "file":
                        self.NODE_LIST.append(sockfd)
                    print "Client "+ type+ str(addr)+" connected to " + self.type
                else:
                    try:
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            print sock.gethostname() + "got data" +data
                            self.broadcast(server_socket,sock,data)
                        else:
                            if sock in self.NODE_LIST:
                                self.NODE_LIST.remove(sock)
                    except:
                        continue

        server_socket.close()

    # broadcast chat messages to all connected clients
    def broadcast(self, server_socket, sock, message):
        print "brodacast called"
        print self.NODE_LIST
        for socket in self.NODE_LIST:
            # send the message only to peer
            if socket != server_socket and socket != sock :
                try :
                    print "trying to send\t" + message
                    socket.send(message)
                except Exception as e:
                    print str(e)
                    # broken socket connection
                    socket.close()
                    # broken socket, remove it
                    if socket in self.NODE_LIST:
                        self.NODE_LIST.remove(socket)

if __name__ == "__main__":
    FileServer(1201,"fileshare")