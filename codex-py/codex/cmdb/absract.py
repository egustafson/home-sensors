# -*- coding: utf-8 -*-
""" Abstract CMDB Repository """

from codex.config import Config, ConfigItem, ManagedObject


class AbstractCMDB(object):

    def __init__(self, config):
        self._config = config

    def get_ci_list(self):
        return []

    def create_ci(self, config):
        ci = ConfigItem(config)
        return ci

    def get_ci(self, oid):
        return ConfigItem(oid)

    def add_config(self, oid, config):
        # append config to ci[oid]
        ver = 0
        return ver

    def get_config(self, oid, ver):
        return ConfigItem(ver)

    def search_ci(self, search_term):
        return ConfigItem(search_term)

    def discover_mo(self, discover_term):
        return ManagedObject(discover_term)

    def get_mo(self, oid):
        return ManagedObject(oid)

    def set_mo_state(self, oid, state):
        return ManagedObject(oid)

    def update_mo_state(self, oid, state):
        return ManagedObject(oid)

    def clear_mo_state(self, oid):
        return ManagedObject(oid)

    def get_mo_status(self, oid):
        status = {}
        return status

    def update_mo_status(self, status):
        return status
