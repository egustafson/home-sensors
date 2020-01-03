# -*- coding: utf-8 -*-
""" CMDB Repository using SQLAlchemy """

import uuid

from codex.config import Config, ConfigItem, ManagedObject
from codex.cmdb.exceptions import CmdbInitializationError

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select, func

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

    ##
    ## Config section
    def cfg_list(self):
        # return the list of CI OIDs
        #>> select distinct oid from ciprops
        sel =  select([ciprops.c.oid]).distinct()
        ll = []
        conn = self._engine.connect()
        try:
            rs = conn.execute(sel)
            for row in rs:
                ll.append(uuid.UUID(row[0]))
        finally:
            conn.close()
        return ll

    def cfg_ver_head(self, oid):
        # return the 'head' (highest & newest) version
        #>> select max(ver) from ciprops where oid=oid
        sel = select([func.max(ciprops.c.ver)]).\
               where(ciprops.c.oid == str(oid))
        ver = 0
        conn = self._engine.connect()
        try:
            ver = conn.execute(sel).scalar()
            if ver is None:
                ver = 0
        finally:
            conn.close()
        return ver

    def cfg_get(self, oid, ver):
        # return the config for oid[ver]
        #>> select key, val from ciprops where oid=oid and ver=ver
        return Config()

    def cfg_append(self, oid, config):
        # append 'config' as the next version of 'oid'
        # return: the version # of the appended config
        ver = self.cfg_ver_head(oid) + 1
        insert_list = []
        for (k, v) in config.as_properties().items():
            insert_list.append(
                {'oid': str(oid), 'ver': ver, 'key': k, 'val': v} )
        if len(insert_list) > 0:
            conn = self._engine.connect()
            conn.execute(ciprops.insert(), insert_list)
            conn.close()
            return ver
        return 0  ## 0 == no insertion

    ##
    ## Tag section
    def tag_list(self, tag):
        # return: list of (oid, ver) for the tag
        return []

    def tag_get_ver(self, oid, tag):
        # return the version with 'tag' on 'oid'
        return 0

    def cfg_get_tags(self, oid):
        # return: list of tags for an oid
        return []

    def set_tag(self, tag, oid, ver):
        # add a tag => oid[ver]
        return None

    ##
    ## Index section
    def mo_discover(self, search):
        # return list[mo] <== 'search' (string)
        return []

    def cfg_search(self, search):
        # return list[ci] <== 'search' (string)
        return []

    ##
    ## Managed Object (MO) section
    def mo_list(self):
        # return a list of oid's that are MO's
        return []

    def mo_get(self, oid):
        # return a ManagedObject
        return ManagedObject(oid)

    def mo_set_props(self, oid, props):
        # set state = 'props' (a PropMap)
        None

    def mo_clear(self, oid):
        # clear all state from MO[oid]
        None




def init_dao(config):
    engine = create_engine(config.get('url'))
    metadata.create_all(engine)
    ##
    ## TODO -
    ##    remove:   Metadata.create_all()
    ##    replace:  sqlalchemy-migrate
    ##      (https://sqlalchemy-migrate.readthedocs.io/en/v0.7.2/versioning.html)
    ##
    return SqlDAO(config, engine)
