#-*- coding: utf-8 -*-
""" Multicast (discovery) listener """

import socket
from socketserver import DatagramRequestHandler, UDPServer


MCAST_ADDR = "239.0.0.1"
MCAST_PORT = 23901
MCAST_TTL  = 5          ## no more than 5 hops through routers



class McastHandler(socketserver.DatagramRequestHandler):
    """
    McastHandler receives discovery requests in the for of JSON text and passes them to
    the CMDB.discover() method.  The result is then returned to the sender as JSON.
    There should be enough information in the response for the requestor to initiate
    further requests through the HTTP-RESTful API.
    """

    def handle(self):
        dgram = self.request[0].rfile.read()
        socket = self.request[1]
        ##
        ## Stub: TODO - implement
        ##
        print("recvfrom({}):  {}".format(self.client_address[0], dgram))
        response = "{}"
        ##
        ##
        socket.sendto(response, self.client_address)


def runMcastService():
    server = UDPServer(MCAST_ADDR, MCAST_PORT, McastHandler)
    ## allow other processes to bind to this port+addr
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ## set packet TTL (hops)
    ttl = struct.pack('b', MCAST_TTL)
    server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    ## disable receiving messages I send (no loopback)
    server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    ## join the multicast group
    group = socket.inet_aton(MULTICAST_ADDR)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    ##
    ## note - all of the above may need to be wrapped into the server_bind()
    ##  method of a derived UDPServer class
    ##
    server.serve_forever()
