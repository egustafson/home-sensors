# *-* coding: utf-8 -*-
""" UnitTest for Propery Map and List """

# ######################################################################
# Test Case thoughts
#
#   basic insert:  map + list
#   complex key insert & extraction (key: kv1.kv2.kv3 ...)
#   complex key  with list in the complex key (i.e. kv1[0].kv2.kv3 ...)
#   Construct from non PropMap & PropList values
#   ingest from json + yaml
#   export to json + yaml
#
#

import unittest

from codex.config.prop import PropMap2 as PropMap
from codex.config.prop import PropList

class TestPropMap(unittest.TestCase):

    def test_simple_keys(self):
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

    def test_compound_keys(self):
        mm = PropMap()
        self.assertTrue(isinstance(mm, PropMap))
        # insertion
        mm['a.b'] = 'val-ab'
        nested = mm.get('a')
        self.assertTrue(isinstance(nested, PropMap))
        self.assertEqual( mm.get('a.b'), nested.get('b'))
        # insertion - 2 deep
        mm['a.b1.b2'] = 'val-ab1b2'
        mm['a.b1.b3'] = 'val-ab1b3'
        n2 = mm.get('a.b1')
        self.assertTrue(isinstance(n2, PropMap))
        self.assertEqual( mm.get('a.b1.b2'), n2.get('b2') )
        self.assertEqual( mm.get('a.b1.b3'), n2.get('b3') )

    def test_construct_from_sequence(self):
        test_vec = (('a','a'), ('b','b'), ('c','c'))
        mm = PropMap(test_vec)
        self.assertEqual( len(test_vec), len(mm) )
        for (k,v) in test_vec:
            self.assertTrue( (k,v) in mm.items() )

    def test_construct_from_dict(self):
        test_dict = { 'a':'a', 'b':'b', 'c':'c' }
        mm = PropMap(test_dict)
        self.assertEqual( len(test_dict), len(mm) )
        for (k,v) in test_dict.items():
            self.assertTrue( (k,v) in mm.items() )

    def test_compound_from_sequence(self):
        test_vec = (('a.b', 'a-b'), ('a.c', 'a-c'), ('b.d', 'b-d'))
        mm = PropMap(test_vec)
        self.assertEqual( len(mm), 2 )
        self.assertEqual( len(mm['a']), 2)
        self.assertEqual( len(mm['b']), 1)
        mm_a = mm['a']
        self.assertEqual( mm['a.b'], mm_a['b'] )
        self.assertEqual( mm['a.c'], mm_a['c'] )
        self.assertEqual( mm['b.d'], mm['b']['d'] )
        for (k,v) in test_vec:
            self.assertEqual( mm[k], v )
            self.assertTrue( (k,v) in mm.items() )

    def test_flatten(self):
        test_vec = (('a.b', 'a-b'), ('a.c', 'a-c'), ('b.d', 'b-d'),
                    ('a.d.e.f', 'a-d-e-f'), ('a.d.e.g', 'a-d-e-g'))
        mm = PropMap(test_vec)
        flat_list = mm.flatten()
        self.assertEqual( len(test_vec), len(flat_list) )
        for (k,v) in test_vec:
            self.assertTrue( (k,v) in flat_list )


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
