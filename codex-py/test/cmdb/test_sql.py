# -*- coding: utf-8 -*-
""" UnitTest for SQL-DAO (SQLAlchemy) """

import unittest

import uuid

from codex.config import Config
from codex.cmdb.sql import init_dao


class TestSqlDAO(unittest.TestCase):

    def setUp(self):
        config = Config()
        config['cmdb.type'] = 'sql'
        config['cmdb.url'] = 'sqlite:///:memory:'
        self.config = config
        #
        config = Config()
        config['key'] = 'value'
        self.t_cfg = config

    def getDao(self, config = None):
        if config is None:
            config = self.config.get('cmdb')
        return init_dao(config)

    def test_construction(self):
        dao = self.getDao()
        self.assertIsNotNone(dao)
        dao.close()

    def test_dump(self):
        dao = self.getDao()
        dao.dump()
        dao.close()

    def test_reset(self):
        dao = self.getDao()
        # empty DAO <- reset
        dao.reset()
        dao.close()

    def test_empty_cfg_list(self):
        dao = self.getDao()
        cl = dao.cfg_list()
        self.assertEqual(len(cl), 0)
        dao.close()

    def test_insert_cfg_list(self):
        dao = self.getDao()
        oid = uuid.uuid1()

        ver = dao.cfg_append(oid, self.t_cfg)
        self.assertEqual(ver, 1)
        cl = dao.cfg_list()
        self.assertEqual(len(cl), 1)
        dao.close()

    def test_insert_update_cfg_list(self):
        dao = self.getDao()
        oid = uuid.uuid1()

        ver = dao.cfg_append(oid, self.t_cfg)
        self.assertEqual(ver, 1)
        cl = dao.cfg_list()
        self.assertEqual(len(cl), 1)
        # insert ver 2
        ver = dao.cfg_append(oid, self.t_cfg)
        self.assertEqual(ver, 2)
        cl = dao.cfg_list()
        # still only one OID in the db
        self.assertEqual(len(cl), 1)
        dao.close()

    def test_multi_insert(self):
        dao = self.getDao()
        oids = []
        for ii in range(0,2):
            oids.append(uuid.uuid1())
        for oid in oids:
            self.t_cfg['k2-oid'] = str(oid)
            dao.cfg_append(oid, self.t_cfg)
        cl = dao.cfg_list()
        for oid in cl:
            self.assertTrue( oid in oids )
        dao.close()
