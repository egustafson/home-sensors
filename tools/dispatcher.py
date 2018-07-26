#!/usr/bin/env python3

class NullEvent:
    def __init__(self):
        self._message = {}
        self._type = "NullEvent"

    def type(self):
        return self._type

    def respond(self, msg):
        ## drop message
        return

class McastEvent:
    def __init__(self, msg, mcast_ep):
        self._message = msg
        self._mcast_ep = mcast_ep

    def respond(self, msg):
        self._mcast_ep.send(msg)



class NullEventHandler:
    def __init__(self):
        return

    def handle(self, event):
        ## do nothing
        return

class Dispatcher:
    def __init__(self):
        self._handlers = []
        return

    def register(self, handler):
        self._handlers.append(handler)

    def unregister(self, handler):
        self._handlers.remove(handler)

    def dispatch(self, event):
        for h in self._handlers:
            h.handle(event)



if __name__ == '__main__':

    r = Dispatcher()
    h = NullEventHandler()
    r.register(h)
    e = NullEvent()
    r.react(e)
    r.unregister(h)

## End of File
