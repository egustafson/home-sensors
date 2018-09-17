# -*- coding: utf-8 -*-
""" Core, CMDB repository """

import uuid

from codex.config import Config


class ConfigItem(object):

    def __init__(self, id):
        self.id = id
        self._cfgs = []
        self._identity = None

    @property
    def config(self):
        cfglen = len(self._cfgs)
        if cfglen < 1:
            return None
        return self._cfgs[cfglen-1]

    @config.setter
    def config(self, value):
        value["_ver"] = len(self._cfgs)
        value["_id"] = self.id
        if '_identity' in value:
            self._identity = value['_identity']
        self._cfgs.append(value)

    def match_identity(self, identity):
        ##
        ## TODO - match all fields before returning true.
        ##
        if self._identity is None or len(self._identity) < 0:
            return False
        config = self.config
        for k in self._identity:
            if k in identity and k in config:
                return (identity[k] == config[k])
        return False


class ResourceType(object): pass


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

def get_cmdb(id=None):
    if _cmdb is None:
        _cmdb = CMDB()
    return _cmdb

