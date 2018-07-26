#!/usr/bin/env python3

from mcast import Mcast

MCAST_PORT  = 10108
MCAST_ADDR  = '224.3.29.71'

if __name__ == '__main__':
    m = Mcast(MCAST_ADDR, MCAST_PORT)
    print('listening on {}:{}'.format(MCAST_ADDR, MCAST_PORT))

    msg = {
        'message': 'value',
        'list': [1,2,3,4],
    }

    print("send: {!r}".format(msg))
    m.send(msg)

    msg2 = m.recv()

    print("recv: {!r}".format(msg2))
    print('done.')

## End of file
