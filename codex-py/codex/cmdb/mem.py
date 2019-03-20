# -*- coding: utf-8 -*-
""" In-Memory CMDB Repository """

import uuid

from codex.config import Config, ConfigItem, ManagedObject

class ConfigsDAO(object):
    """ Abstract the 'configs' table.
          configs[oid][ver] -> config
    """

    def __init__(self):
        self._configs = {}

    def get_list(self):
        return list(self._configs.keys())

    def get_count(self, oid):
        cnt = len(self._configs.get(oid, []))
        return cnt

    def get_config(self, oid, ver):
        cfgs = self._configs.get(oid, [])
        if len(cfgs) <= ver:
            return None
        return cfgs[ver]

    def append(self, oid, config):
        cfglist = self._configs.get(oid, None)
        if cfglist is None:
            cfglist = []
            self._configs[oid] = cfglist
        config["_id"] = oid
        ver = len(cfglist)     # version starts at zero
        config["_ver"] = ver
        self._configs[oid].append(config)
        return ver


class TagsDAO(object):
    """ Abstract the 'tags' table
          tags[tag][oid] -> version
    """

    def __init__(self):
        self._tags = {}

    def get_oids(self, tag):
        oids = self._tags.get(tag, {})
        return oids.keys()

    def get_version(self, oid, tag):
        oids = self._tags.get(tag, {})
        if len(oids) < 1:
            return None
        return oids.get(oid, None)

    def get_tags(self, oid):
        taglist = []
        for (tag, o) in self._tags.items():
            if oid in o:
                taglist.append(tag)
        return taglist

    def set_tag(self, oid, tag, ver):
        oids = self._tags.get(tag, None)
        if oids is None:
            oids = {}
            self._tags[tag] = oids
        oids[oid] = ver

class IndexDAO(object):
    pass

class MObjsDAO(object):
    """ Abstract the 'mobjs' table
          mobjs[oid] -> state
    """

    def __init__(self):
        self._mobjs = {}

    def get_list(self):
        return self._mobjs.keys()

    def get_state(self, oid):
        return self._mobjs.get(oid, None)

    def set_state(self, oid, state):
        self._mobjs[oid] = state

    def clear(self, oid):
        self._mobjs.pop(oid, None)


class MemoryDAO(object):

    def __init__(self, config):
        self._config = config
        self._configs = ConfigsDAO()
        self._tags = TagsDAO()
        self._indexs = IndexDAO()
        self._mobjs = MObjsDAO()

    @property
    def configs(self):
        return self._configs

    @property
    def tags(self):
        return self._tags

    @property
    def indexes(self):
        return self._indexes

    @property
    def mobjs(self):
        return self._mobjs
