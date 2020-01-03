# -*- coding: utf-8 -*-
""" healthz application health object """


class _Healthz():

    def status(self):
        return { 'status': "ok" }


_HEALTHZ = None


def Healthz():
    """ factory function to return singleton """
    global _HEALTHZ
    if _HEALTHZ is None:
        _HEALTHZ = _Healthz()
    return _HEALTHZ
