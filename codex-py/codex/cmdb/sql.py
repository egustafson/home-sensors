# -*- coding: utf-8 -*-
""" CMDB Repository using SQLAlchemy """

import uuid

from codex.config import Config, ConfigItem, ManagedObject
from codex.cmdb.exceptions import CmdbInitializationError

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select

metadata = MetaData()
ciprops = Table('ciprops', metadata,
    Column('id', Integer, primary_key=True),
    Column('oid', String),
    Column('ver', Integer),
    Column('key', String),
    Column('val', String),
)

tags = Table('tags', metadata,
    Column('id', Integer, primary_key=True),
    Column('oid', String),
    Column('tag', String),
    Column('ver', Integer),
)

moprops = Table('moprops', metadata,
    Column('id', Integer, primary_key=True),
    Column('oid', String),
    Column('key', String),
    Column('val', String),
)


class SqlDAO(object):

    def __init__(self, config, engine):
        self._config = config
        self._engine = engine

    def close(self):
        self._engine.dispose()
        self._engine = None

    def reset(self):
        conn = self._engine.connect()
        conn.execute(ciprops.delete())
        conn.execute(tags.delete())
        conn.execute(moprops.delete())
        conn.close()

    def dump(self):
        conn = self._engine.connect()
        try:
            rs = conn.execute(select([ciprops]))
            print("Table: ciprops")
            for row in rs:
                print(row)
            rs = conn.execute(select([tags]))
            print("Table: tags")
            for row in rs:
                print(row)
            rs = conn.execute(select([moprops]))
            print("Table: moprops")
            for ros in rs:
                print(row)
        finally:
            conn.close()


def init_dao(config):
    engine = create_engine(config.get('url'))
    metadata.create_all(engine)
    return SqlDAO(config, engine)
