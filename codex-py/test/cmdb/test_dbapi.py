# -*- coding: utf-8 -*-
""" UnitTest for Python DB-API (sqlite3) """

import unittest

from codex.config import Config
from codex.cmdb import init_cmdb


class TestDbApiCMDB(unittest.TestCase):

    def test_construction(self):
        config = Config()
        config['cmdb.type'] = 'dbapi'
        config['cmdb.db-type'] = 'sqlite3'
        config['cmdb.uri'] = ':memory:'
        cmdb = init_cmdb(config)
        self.assertIsNotNone(cmdb)
        cmdb.close()
