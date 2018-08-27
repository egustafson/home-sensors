# -*- coding: utf-8 -*-
""" Core, CMDB repository """


class Config(dict): pass
""" A configuration object -- initially a dict (a hack)
       see: https://configtree.readthedocs.io/en/latest/
       and: http://www.kr41.net/2015/06-15-about_configtree.html
    The 'final' object should support nested dict and array
    objects, but that's *hard* -- so start with the hack of
    using a python dict.
"""

class Resource(object):

    def __init__(self, id):
        self.id = id
        self._cfg = None
        self._cfg_ver = 0
        self.identity = None

    @property
    def meta(self):
        """meta information about the Resource."""
        m = {
            'id': self.id,
            'ver': self._cfg_ver
        }
        return m

    @property
    def config(self):
        return self._cfg

    @config.setter
    def config(self, value):
        self._cfg_ver += 1
        self._cfg = value
        if '_identity' in self._cfg:
            self._identity = self._cfg['_identity']

    def match_identity(self, identity):
        if self._identity is None:
            return False
        for (k, v) in self._identity.items():
            if k in identity:
                return (identity[k] == v)
        return False


class Link(object): pass

class ResourceType(object): pass


class CMDB(object):

    def __init__(self):
        self.resources = { }
        self.links = { }

    def set_config(self, resource_id, config):
        r = self.resources.get(resource_id)
        if r is None:
            r = Resource(resource_id)
            self.resources[resource_id] = r
        r.config = config
        return r.meta

    def get_config(self, resource_id):
        r = self.resources.get(resource_id)
        if r is None:
            return None
        return r.config

    def discover(self, identity):
        for (id, r) in self.resources.items():
            if r.match_identity(identity):
                return r.meta
        return None



###

_cmdb = None

def get_cmdb(id=None):
    if _cmdb is None:
        _cmdb = CMDB()
    return _cmdb

