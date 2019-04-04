# -*- coding: utf-8 -*-
""" UnitTest for SQL-DAO (SQLAlchemy) """

import unittest

from codex.config import Config
from codex.cmdb import init_cmdb


class TestSqlCMDB(unittest.TestCase):

    def test_construction(self):
        config = Config()
        config['cmdb.type'] = 'sql'
        config['cmdb.url'] = 'sqlite:///:memory:'
        cmdb = init_cmdb(config)
        self.assertIsNotNone(cmdb)
        cmdb.close()
