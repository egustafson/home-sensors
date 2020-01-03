# -*- coding: utf-8 -*-
""" Core, CMDB repository """

import uuid

from codex.config import Config, ConfigItem

from codex.cmdb.exceptions import CmdbInitializationError
from codex.cmdb.cmdb import CMDB
from codex.cmdb.mem import MemoryDAO  ## TODO - fix to use init_dao()
from codex.cmdb.sql import init_dao as init_sql_dao


_CMDB = None

def init_cmdb(cfg):
    global _CMDB
    if _CMDB is not None:
        raise RuntimeError("CMDB already initialized.")
    cmdb_type = cfg.get('cmdb.type')
    if cmdb_type is None:
        raise CmdbInitializationError("config does not define 'cmdb.type'")
    if cmdb_type == 'memory':
        dao = MemoryDAO(cfg.get('cmdb'))
    if cmdb_type == 'sql':
        dao = init_sql_dao(cfg.get('cmdb'))
        # raise CmdbInitializationError('sqlite CMDB DAO not supported yet')
    if dao is None:
        raise CmdbInitializationError("Unknown cmdb.type ({})".format(cmdb_type))
    return CMDB(dao, cfg.get('cmdb'))


def get_cmdb():
    global _CMDB
    if _CMDB is None:
        raise CmdbInitializationError("CMDB not initialized.")
    return _CMDB
