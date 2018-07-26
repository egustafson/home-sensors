#!/usr/bin/env python3

import json
import socket
import struct


class Mcast:

    def __init__(self, mcast_addr, port):
        self.mcast_group = (mcast_addr, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ## allow multiple processes to bind to this port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))
        ## set sending packet ttl
        ttl = struct.pack('b', 1) ## 1 hop (no router fwd)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        ## disable receiving messages I send
        #self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
        ## Join the mcast group
        group = socket.inet_aton(mcast_addr)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def close(self):
        self.sock.close()

    def send(self, msg):
        tx = msg
        if isinstance(tx, dict):
            tx = json.dumps(tx, separators=(',',':'))
        if isinstance(tx, str):
            tx = tx.encode('utf-8')
        return self.sock.sendto(tx, self.mcast_group)

    ##
    ## TODO - track sent messages and don't return them w/ recv()
    ##   - then re-enable socket.IP_MULTICAST_LOOP
    ##

    def recv(self):
        (rx, addr) = self.sock.recvfrom(8192)
        rx = json.loads(rx)
        rx['_recvfrom'] = {}
        rx['_recvfrom']['addr'] = addr[0]
        rx['_recvfrom']['port'] = addr[1]
        return rx

## End of file
