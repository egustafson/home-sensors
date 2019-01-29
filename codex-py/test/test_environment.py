# -*- coding: utf-8 -*-
""" UnitTest for codex.cmdb """

import unittest

class TestEnvironment(unittest.TestCase):

    def test_python3(self):
        import sys
        major, minor, micro, releaselevel, serial = sys.version_info
        self.assertGreaterEqual( major, 3 )
