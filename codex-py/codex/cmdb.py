# -*- coding: utf-8 -*-
""" Core, CMDB repository """

class CodexCMDB(object):

    def __init__(self):
        self.bogus = "bogus"



###

_cmdb = CodexCMDB()

def get_codex():
    return _cmdb
