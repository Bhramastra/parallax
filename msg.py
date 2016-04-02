import thread
import sys
import socket
import select



class Server:
    SOCKET_LIST = []
    HOST = '0.0.0.0'
    RECV_BUFFER = 4096
    port= 1200
    type= 'master'

    def __init__(self, port, type):
        self.port=port
        self.type=type
        if type=="fileshare":
            self.RECV_BUFFER=1
        self.server()

    def server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.HOST, self.port))
        server_socket.listen(10)

        # add server socket object to the list of readable connections
        self.SOCKET_LIST.append(server_socket)

        print "%s server started on port %s" % (self.type, str(self.port))

        while 1:

            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select(self.SOCKET_LIST,[],[],0)

            for sock in ready_to_read:
                # a new connection request recieved
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    # type=sockfd.recv(1024)
                    # print type
                    # if type == "node":
                    #     NODE_LIST.append(sockfd)
                    # if type == "scheduler":
                    #     SCHEDULER_LIST.append(sockfd)
                    # if type == "user":
                    #     USER_LIST.append(sockfd)
                    self.SOCKET_LIST.append(sockfd)
                    print "Client "+ str(addr)+" connected to " +self.type

                   # broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

                # a message from a client, not a new connection
                else:
                    # process data recieved from client,
                    try:
                        # receiving data from the socket.
                        data = sock.recv(self.RECV_BUFFER)
                        if data:
                            # there is something in the socket
                            print "received" + data
                            self.broadcast(server_socket,sock,data)
                        else:
                            # remove the socket that's broken
                            if sock in self.SOCKET_LIST:
                                self.SOCKET_LIST.remove(sock)

                            # at this stage, no data means probably the connection has been broken
                           # broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)

                    # exception
                    except:
                       # broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                        continue

        server_socket.close()

    # broadcast chat messages to all connected clients
    def broadcast(self, server_socket, sock, message):
        print "brodacast called"
        print self.SOCKET_LIST
        for socket in self.SOCKET_LIST:
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
                    if socket in self.SOCKET_LIST:
                        self.SOCKET_LIST.remove(socket)
