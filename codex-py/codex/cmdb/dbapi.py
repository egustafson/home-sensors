# -*- cod}ing: utf-8 -*-
""" CMDB Repository using Python DB-API (PEP-249) """

import uuid

from codex.config import Config, ConfigItem, ManagedObject
from codex.cmdb.exceptions import CmdbInitializationError

class DbApiDAO(object):

    def __init__(self, config, conn):
        self._config = config
        self._conn = conn

    def close(self):
        self._conn.close()
        self._conn = None

    def reset(self):
        pass


def init_sqlite3(config):
    import sqlite3
    uri = config.get('uri')
    conn = sqlite3.connect(uri, uri=True)
    return conn


def init_dao(config):
    db_switch = {
        'sqlite3': init_sqlite3,
    }
    dbtype = config.get('db-type')
    initializer = db_switch.get(dbtype)
    if initializer is None:
        msg = "Unknown DB type '{}'".format(dbtype)
        raise CmdbInitializationError(msg)
    connection = initializer(config)
    return DbApiDAO(config, connection)
