#-*- coding: utf-8 -*-
""" Multicast (discovery) listener """

import logging
import socket
import struct
from socketserver import DatagramRequestHandler, UDPServer
from threading import Thread

from codex.cmdb import get_cmdb

logger = logging.getLogger(__name__)


MCAST_ADDR = '239.0.0.1'
MCAST_PORT = 23901
MCAST_TTL  = 5          ## no more than 5 hops through routers

## 19 Sep 2018 -- Note
##
##  I am returning to the mcast section of this.  After review, this code dev
## came after the work in tools/mcast.py and is my preferred strategy.
## There may be some insight from the tools/mcast.py code that hasn't been
## factored in so review.
##


class McastHandler(DatagramRequestHandler):
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

class McastThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="McastServer")
        self.server = UDPServer((MCAST_ADDR, MCAST_PORT), McastHandler)
        ## allow other processes to bind to this port+addr
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ## set packet TTL (hops)
        ttl = struct.pack('b', MCAST_TTL)
        self.server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        ## disable receiving messages I send (no loopback)
        self.server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        ## join the multicast group
        group = socket.inet_aton(MCAST_ADDR)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.server.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        ##
        ## note - all of the above may need to be wrapped into the server_bind()
        ##  method of a derived UDPServer class
        ##
        logger.info("McastServer thread initialized with config: ...")

    def run(self):
        logger.debug("McastServer thread started.")
        self.server.serve_forever()
