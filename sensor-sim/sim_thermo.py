#!/usr/bin/env python3

def discover(cfg):
    pass

class Logger():  ## mimic logger in device
    def __init__(self):
        self._q = []
        self._mq = None

    def set_mq(self, mq, topic):
        self._mq = mq
        self._topic = topic
        while m in self._q:
            self._send(m)

    def _send(self, msg):
        if self._mq:
            self._mq.publish(self._topic, msg)
        else:
            self.fatal('Logger._send() invoked with no mq')

    def log(self, msg):
        print("LOG:  {}".format(msg))
        if self._mq:
            self._send(msg)
        else:
            self._q.append(msg)

    def fatal(self, msg):
        print("FATAL: {}".format(msg))
        raise "fatal() invoked, bailing out"


if __name__=='__main__':

    # initialize logging
    log = Logger()

    # bootstrap network/wifi -- nothing to do

    # discover CMDB and identity

    # load config from CMDB using discovered identity

    # initialize mqtt connection

    # (pseudo) initialize sensor hardware

    # ?? pivot logging to mqtt / enable mqtt logging

    # initialize structures for data logging

    # loop forever -- sample & report (to mqtt)

    print('done.')
