# -*- coding: utf-8 -*-
""" Core, CMDB repository """

import uuid

from codex.config import Config, ConfigItem

from codex.cmdb.cmdb import CMDB
from codex.cmdb.mem import MemoryDAO
#from codex.cmdb.sqlite import SqliteDAO


class OldCMDB(object):

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


class CmdbInitializationError(Exception):
    pass

def get_cmdb():
    global _cmdb
    if _cmdb is None:
        raise CmdbInitializationError("CMDB not initialized.")
    return _cmdb


def init_cmdb(cfg=None):
    global _cmdb
    if _cmdb is not None:
        raise RuntimeError("CMDB already initialized.")
    if cfg is None:
        _cmdb = OldCMDB()
        return True
    cmdb_type = cfg.get('cmdb.type')
    if cmdb_type is None:
        raise CmdbInitializationError("config does not define 'cmdb.type'")
    if cmdb_type == 'memory':
        dao = MemoryDAO(cfg.get('cmdb'))
    if cmdb_type == 'sqlite':
        # dao = SqliteDAO(cfg.get('cmdb'))
        raise CmdbInitializationError('sqlite CMDB DAO not supported yet')
    if dao is None:
        raise CmdbInitializationError("Unknown cmdb.type ({})".format(cmdb_type))
    return CMDB(dao, cfg.get('cmdb'))
