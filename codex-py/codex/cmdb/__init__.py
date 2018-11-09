# -*- coding: utf-8 -*-
""" Core, CMDB repository """

import uuid

from codex.config import Config, ConfigItem


class CMDB(object):

    def __init__(self):
        self.configitems = { }

    def reset(self):
        self.configitems = { }

    def list(self):
        return list(self.configitems.keys())

    def add_config(self, config):
        id = uuid.uuid1()
        ci = ConfigItem(id)
        self.configitems[id] = ci
        ci.config = config
        return ci.config

    def set_config(self, id, config):
        r = self.configitems.get(id)
        if r is None:
            r = ConfigItem(id)
            self.configitems[id] = r
        r.config = config
        return r.config

    def get_config(self, id):
        r = self.configitems.get(id)
        if r is None:
            return None
        return r.config

    def discover(self, identity):
        for (id, r) in self.configitems.items():
            if r.match_identity(identity):
                return r.config
        return None



###

_cmdb = None


def get_cmdb():
    global _cmdb
    if _cmdb is None:
        init_cmdb()
    return _cmdb


def init_cmdb(cfg=None):
    global _cmdb
    if _cmdb is not None:
        raise RuntimeError("CMDB already initialized.")
    _cmdb = CMDB()
    return True
