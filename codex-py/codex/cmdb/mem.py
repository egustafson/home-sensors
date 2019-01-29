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


class MemoryCMDB(object):
    """ An In-Memory CMDB """

    def __init__(self, config):
        self._config = config
        self._oper_tag = self._config.get("operational-tag", "operational")
        self._configsDao = ConfigsDAO()
        self._tagsDao = TagsDAO()
        self._indexDao = IndexDAO()
        self._mobjsDao = MObjsDAO()

    def _version(self, oid, tag="_head"):
        if isinstance(tag, int):
            return tag
        ver = -1
        if len(tag) < 1 or tag == "_head":
            ver = self._configsDao.get_count(oid) - 1
        else:
            ver = self._tagsDao.get_version(oid, tag)
        if ver < 0:
            return None
        return ver

    def ci_list(self):
        return self._configsDao.get_list()

    def ci_get(self, oid, tag="_head"):
        v = self._version(oid, tag)
        if v != None:
            return self._configsDao.get_config(oid, v)
        #
        # Log a problem.  Invalid tag/version or OID
        #
        return None

    def ci_new(self, config):
        oid = uuid.uuid1()
        self._configsDao.append(oid, config)
        return oid

    def ci_update(self, oid, config):
        self._configsDao.append(oid, config)
        return ver

    def ci_search(self, search_term):
        #
        # TODO
        #
        return None

    def mo_discover(self, discover_term):
        #
        # TODO
        #
        return None

    def mo_list(self):
        return self._mobjsDao.get_list()

    def mo_get(self, oid):
        state = self._mobjsDao.get_state(oid)
        if state is None:
            return None
        mo = ManagedObject(oid, oid)
        mo.state = state
        ver = self._version(oid, self._oper_tag)
        if ver != None:
            cfg = self._configsDao.get_config(oid, ver)
            mo.config = cfg
        return mo

    def mo_set(self, oid, state):
        self._mobjsDao.set_state(oid, state)
        return self.get_mo(oid)

    def mo_update(self, oid, state):
        #
        # TODO
        #
        return self.get_mo(oid)

    def mo_destroy(self, oid):
        self._mobjsDao.clear(oid)
