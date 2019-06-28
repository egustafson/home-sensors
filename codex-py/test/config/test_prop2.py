# *-* coding: utf-8 -*-
""" UnitTest for Propery Map and List """

## Alternative PropMap implementation -- prop2.py

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

from codex.config.prop2 import PropMap
from codex.config.prop2 import PropList

class TestPropMap(unittest.TestCase):

#    def test_simple_keys(self):
#        mm = PropMap()
#        # insertion
#        mm['a'] = 'a'
#        self.assertEqual(len(mm), 1)
#        mm['b'] = 'b'
#        self.assertEqual(len(mm), 2)
#        # retreival
#        self.assertEqual(mm.get('a'), 'a')
#        self.assertEqual(mm.get('b'), 'b')
#        # removal
#        del mm['a']
#        self.assertEqual(len(mm), 1)
#        self.assertTrue(('b','b') in mm.items())

    def test_immutable(self):
        mm = PropMap()   ## an immutable PropMap
        with self.assertRaises(TypeError):
            mm['a'] = 'foo'  ## should throw

    def test_compound_keys(self):
        test_dict = {
            'a.b': 'val-ab',
            'a.b1.b2': 'val-ab1b2',
            'a.b1.b3': 'val-ab1b3'
        }
        mm = PropMap().load(test_dict)
        self.assertTrue(isinstance(mm, PropMap))
        nested = mm.get('a')
        self.assertTrue(isinstance(nested, PropMap))
        self.assertEqual( mm.get('a.b'), nested.get('b'))
        n2 = mm.get('a.b1')
        self.assertTrue(isinstance(n2, PropMap))
        self.assertEqual( mm.get('a.b1.b2'), n2.get('b2') )
        self.assertEqual( mm.get('a.b1.b3'), n2.get('b3') )

    def test_construct_from_sequence(self):
        test_vec = (('a','a'), ('b','b'), ('c','c'))
        mm = PropMap().load(test_vec)
        self.assertEqual( len(test_vec), len(mm) )
        for (k,v) in test_vec:
            self.assertTrue( (k,v) in mm.items() )

    def test_construct_from_dict(self):
        test_dict = { 'a':'a', 'b':'b', 'c':'c' }
        mm = PropMap().load(test_dict)
        self.assertEqual( len(test_dict), len(mm) )
        for (k,v) in test_dict.items():
            self.assertTrue( (k,v) in mm.items() )

    def test_compound_from_sequence(self):
        test_vec = (('a.b', 'a-b'), ('a.c', 'a-c'), ('b.d', 'b-d'))
        mm = PropMap().load(test_vec)
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

    def test_as_properties(self):
        test_vec = (('a.b', 'a-b'), ('a.c', 'a-c'), ('b.d', 'b-d'),
                    ('a.d.e.f', 'a-d-e-f'), ('a.d.e.g', 'a-d-e-g'))
        mm = PropMap().load(test_vec)
        flat_props = mm.as_properties()
        flat_list = flat_props.items()
        self.assertEqual( len(test_vec), len(flat_list) )
        for (k,v) in test_vec:
            self.assertTrue( (k,v) in flat_list )

class TestPropList(unittest.TestCase):

    def test_immutable(self):
        ll = PropList()
        with self.assertRaises(TypeError):
            ll[0] = 'foo'   ## should throw

    def test_simple(self):
        test_list = ('a', 'b', 'c')
        ll = PropList().load(test_list)
        self.assertEqual( len(test_list), len(ll) )
        self.assertEqual( ll[0], test_list[0] )
        for v in ll:
            self.assertTrue( v in test_list )
        for v in test_list:
            self.assertTrue( v in ll )

    def test_map_list(self):
        test_map = {
            'a': ['a', 'b', 'c'],
            'c': 'simple-value'
        }
        mm = PropMap().load(test_map)
        self.assertEqual( len(test_map), len(mm) )
        self.assertEqual( len(test_map['a']), len(mm['a']) )
        for v in mm['a']:
            self.assertTrue( v in test_map['a'] )
        self.assertEqual( mm['a'][0], test_map['a'][0] )
        self.assertEqual( mm['a.0'], test_map['a'][0] )
        self.assertEqual( mm['a[0]'], test_map['a'][0] )
        self.assertEqual( mm['a.[0]'], test_map['a'][0] )

    def test_map_list_list(self):
        test_map = {
            'a': [ ['a', 'b'], 'c', ['d', 'e'] ],
            'x': 'simple-value'
        }
        mm = PropMap().load(test_map)
        self.assertEqual( len(test_map), len(mm) )
        self.assertEqual( len(test_map['a']), len(mm['a']) )
        self.assertEqual( mm['a'][0][0], test_map['a'][0][0] )
        self.assertEqual( mm['a.0'][0],  test_map['a'][0][0] )
        self.assertEqual( mm['a.0.0'],  test_map['a'][0][0] )
        self.assertEqual( mm['a[0].0'],  test_map['a'][0][0] )
        self.assertEqual( mm['a[0][0]'],  test_map['a'][0][0] )
        self.assertEqual( mm['a[0].[0]'],  test_map['a'][0][0] )
        self.assertEqual( mm['a.0.[0]'],  test_map['a'][0][0] )
        self.assertEqual( mm['a.0[0]'],  test_map['a'][0][0] )
        self.assertEqual( mm['a.2.1'], test_map['a'][2][1] )

    #@unittest.skip("index in middle of key - still broken")
    def test_from_properties(self):
        test_map = {
            'a[0]': 'a-zero',
            'a[1]': 'a-one',
            'a.2' : 'a-two',
            'b'   : 'bee'
        }
        mm = PropMap().load(test_map)
        self.assertEqual( mm['a'][0], test_map['a[0]'])
        self.assertEqual( mm['a'][1], test_map['a[1]'])
        self.assertEqual( mm['a'][2], test_map['a.2'])
