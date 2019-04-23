# -*- coding: utf-8 -*-
""" UnitTest for CMDB(SQL-DAO) (SQLAlchemy) """

import unittest

from codex.config import Config
from codex.cmdb import init_cmdb


class TestCMDB(unittest.TestCase):

    def setUp(self):
        config = Config()
        config['cmdb.type'] = 'sql'
        config['cmdb.url'] = 'sqlite:///:memory:'
        self.config = config

    def test_construction(self):
        cmdb = init_cmdb(self.config)
        self.assertIsNotNone(cmdb)
        cmdb.close()

    def test_dump(self):
        cmdb = init_cmdb(self.config)
        cmdb.dump()
        cmdb.close()

#    def test_cfg_list(self):
#        cmdb = init_cmdb(self.config)
#        cmdb.close()
