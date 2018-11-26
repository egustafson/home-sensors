# *-* coding: utf-8 -*-
""" UnitTest for Propery Map and List """

import unittest

from codex.config.prop import PropMap
from codex.config.prop import PropList


class TestPropMap(unittest.TestCase):

    def test_basic_map(self):
        mm = PropMap()
        # insertion
        mm['a'] = 'a'
        self.assertEqual(len(mm), 1)
        mm['b'] = 'b'
        self.assertEqual(len(mm), 2)
        # retreival
        self.assertEqual(mm.get('a'), 'a')
        self.assertEqual(mm.get('b'), 'b')
        # removal
        del mm['a']
        self.assertEqual(len(mm), 1)
        self.assertTrue(('b','b') in mm.items())

    def test_construct_map(self):
        test_vec = (('a','a'), ('b','b'), ('c','c'))
        mm = PropMap(test_vec)
        self.assertEqual( len(test_vec), len(mm) )
        for (k,v) in test_vec:
            self.assertTrue( (k,v) in mm.items() )


class TestPropList(unittest.TestCase):

    def test_basic_list(self):
        ll = PropList()
        lt = []
        for ii in range(1,9):
            ll.append(ii)
            lt.append(ii)
        while len(ll) > 0:
            self.assertEqual( ll.pop(), lt.pop() )

    def test_index_list(self):
        ll = PropList(range(10))
        self.assertEqual(len(ll), 10)
        for ii in range(10):
            ll[ii] = ii
        for ii in range(0,len(ll)-1):
            self.assertEqual( ii, ll[ii] )
