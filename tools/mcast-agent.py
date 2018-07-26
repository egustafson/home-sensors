#!/usr/bin/env python3

import socket
import struct
import sys

MCAST_PORT  = 10108
MCAST_ADDR  = '224.3.29.71'


class McastEndpoint:

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
        return self.sock.sendto(msg, self.mcast_group)

    def recvfrom(self):
        return self.sock.recvfrom(8192)


if __name__ == '__main__':
    mep = McastEndpoint(MCAST_ADDR, MCAST_PORT)
    print('listening on {}:{}'.format(MCAST_ADDR, MCAST_PORT))

    sent = mep.send('simple message'.encode('utf-8'))
    print("sent: {}".format(sent))

    while True:
        try:
            (data, addr) = mep.recvfrom()
        except socket.timeout:
            print('timeout')
        else:
            print("recvfrom{}: {}".format(addr, data.decode()))

    mep.close() ## we never hit this point.

## End of file
