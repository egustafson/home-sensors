# -*- coding: utf-8 -*-
""" UnitTest for In-Memory CMDB """

import unittest

from codex.config import Config

from codex.cmdb.mem import MemoryCMDB


config = Config()

class TestMemCMDB(unittest.TestCase):

    def test_construction(self):
        cmdb = MemoryCMDB(config)
        self.assertIsNotNone(cmdb)

    def test_ci_operations(self):
        cmdb = MemoryCMDB(config)
        self.assertEqual( len(cmdb.get_ci_list()), 0 )
        oid = cmdb.create_ci(config)
        # print("oid = {}".format(oid))
        cilist = cmdb.get_ci_list()
        self.assertEqual( len(cilist), 1)
        self.assertEqual( oid, cilist[0] )
        cfg = cmdb.get_config(oid, 0)
        # print("\ncfg = {")
        # for (k,v) in cfg.items():
        #     print("  {}: {},".format(k,v))
        # print("}")
        self.assertEqual( len(cfg), 2 )
