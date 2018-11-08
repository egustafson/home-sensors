# -*- coding: utf-8 -*-
""" UnitTest for codex.cmdb """

import unittest
import uuid

from codex.cmdb import CMDB


class TestCMDB(unittest.TestCase):

    def setUp(self):
        self.cmdb = CMDB()
        self.config = {
            '_identity': {
                'serial': '10101'
            },
            'serial': '10101',
            'test-key': 'test-value'
        }

    def test_python3(self):
        import sys
        major, minor, micro, releaselevel, serial = sys.version_info
        self.assertGreaterEqual( major, 3 )

    def test_put_get_config(self):
        #
        # test - put
        #
        t_config = self.config
        t_resource_id = uuid.uuid1()
        meta = self.cmdb.set_config(t_resource_id, t_config)
        self.assertIsNotNone(meta)
        self.assertTrue( meta['_id'] == t_resource_id )
        #
        # test - get  (what was put)
        #
        stored_config = self.cmdb.get_config(t_resource_id)
        self.assertIsNotNone(stored_config)
        self.assertEqual(stored_config, t_config)


    def test_discover(self):
        t_config = self.config
        created_meta = self.cmdb.set_config(uuid.uuid1(), t_config)
        self.assertIsNotNone(created_meta)
        #
        serial_no = t_config['_identity']['serial']
        identity = { 'serial': serial_no }
        print('identity: {}'.format(identity))
        discovered_meta = self.cmdb.discover( identity )
        self.assertIsNotNone(discovered_meta)
        self.assertEqual(discovered_meta['_id'], created_meta['_id'])


