# -*- coding: utf-8 -*-
""" Config Item """

#from codex.config import Config

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

