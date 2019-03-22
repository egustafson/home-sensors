# -*- coding: utf-8 -*-
""" CMDB Interface """

import uuid

from codex.config import Config, ConfigItem, ManagedObject


class CMDB(object):
    """ An In-Memory CMDB """

    def __init__(self, dao, config):
        self._dao = dao
        self._config = config
        self._oper_tag = self._config.get("operational-tag", "operational")

    def _version(self, oid, tag="_head"):
        if isinstance(tag, int):
            return tag
        ver = -1
        if len(tag) < 1 or tag == "_head":
            ver = self._dao.configs.get_count(oid) - 1
        else:
            ver = self._dao.tags.get_version(oid, tag)
        if ver < 0:
            return None
        return ver

    def close(self):
        self._dao.close()
        self._dao = None
        self._config = None

    def reset(self):
        self._dao.reset()
        

    def ci_list(self):
        return self._dao.configs.get_list()

    def ci_get(self, oid, tag="_head"):
        v = self._version(oid, tag)
        if v != None:
            return self._dao.configs.get_config(oid, v)
        #
        # Log a problem.  Invalid tag/version or OID
        #
        return None

    def ci_new(self, config):
        oid = uuid.uuid1()
        self._dao.configs.append(oid, config)
        return oid

    def ci_update(self, oid, config):
        self._dao.configs.append(oid, config)
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
        return self._dao.mobjs.get_list()

    def mo_get(self, oid):
        state = self._dao.mobjs.get_state(oid)
        if state is None:
            return None
        mo = ManagedObject(oid, oid)
        mo.state = state
        ver = self._version(oid, self._oper_tag)
        if ver != None:
            cfg = self._dao.configs.get_config(oid, ver)
            mo.config = cfg
        return mo

    def mo_set(self, oid, state):
        self._dao.mobjs.set_state(oid, state)
        return self.get_mo(oid)

    def mo_update(self, oid, state):
        #
        # TODO
        #
        return self.get_mo(oid)

    def mo_destroy(self, oid):
        self._dao.mobjs.clear(oid)
