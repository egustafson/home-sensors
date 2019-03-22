# -*- coding: utf-8 -*-
""" UnitTest for In-Memory CMDB """

import unittest

from codex.config import Config
from codex.cmdb import init_cmdb


class TestMemCMDB(unittest.TestCase):

    def test_construction(self):
        config = Config()
        config['cmdb.type'] = 'memory'
        cmdb = init_cmdb(config)
        self.assertIsNotNone(cmdb)
        cmdb.close()

    def test_ci_operations(self):
        config = Config()
        config['cmdb.type'] = 'memory'
        cmdb = init_cmdb(config)

        self.assertEqual( len(cmdb.ci_list()), 0 )
        oid = cmdb.ci_new(Config())
        # print("oid = {}".format(oid))
        cilist = cmdb.ci_list()
        self.assertEqual( len(cilist), 1)
        self.assertEqual( oid, cilist[0] )
        cfg = cmdb.ci_get(oid, 0)
        # print("\ncfg = {")
        # for (k,v) in cfg.items():
        #     print("  {}: {},".format(k,v))
        # print("}")
        self.assertEqual( len(cfg), 2 )
        cmdb.close()
