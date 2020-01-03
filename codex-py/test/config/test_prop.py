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

from codex.config.prop import PropMap
from codex.config.prop import PropList

class TestPropMap(unittest.TestCase):

    def test_simple_insertion(self):
        mm = PropMap()
        mm['a'] = 'a-value'
        self.assertTrue( 'a' in mm )
        self.assertEqual( mm['a'], 'a-value' )

    def test_nested_insertion(self):
        mm = PropMap()
        mm['a.b.c'] = 'c-value'
        self.assertTrue( 'a' in mm )
        self.assertTrue( 'a.b' in mm )
        self.assertTrue( 'a.b.c' in mm )
        self.assertTrue(isinstance(mm.get('a'), PropMap))
        self.assertTrue(isinstance(mm.get('a.b'), PropMap))
        self.assertEqual( mm.get('a.b.c'), 'c-value' )
        self.assertEqual( mm['a.b.c'], 'c-value' )

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

    def test_overlap_nested_insertion(self):
        mm = PropMap()
        mm['a.b.c1'] = 'c1-value'
        mm['a.b.c2'] = 'c2-value'
        mm['a.b2'] = 'b2-value'
        self.assertEqual( mm.get('a.b.c1'), 'c1-value')
        self.assertEqual( mm.get('a.b.c2'), 'c2-value')
        self.assertEqual( mm.get('a.b2'), 'b2-value')

    def test_key_error(self):
        mm = PropMap()
        self.assertTrue( 'bogus-key' not in mm )
        with self.assertRaises(KeyError):
            mm['bogus-key']

    def test_simple_deletion(self):
        mm = PropMap()
        mm['a1'] = 'a1-value'
        mm['a2'] = 'a2-value'
        self.assertEqual( len(mm), 2)
        del mm['a1']
        self.assertEqual( len(mm), 1)
        self.assertTrue( 'a1' not in mm )
        self.assertTrue( 'a2' in mm )
        self.assertEqual( mm.get('a2'), 'a2-value' )

    def test_nested_deletion(self):
        mm = PropMap()
        mm['a.b.c1'] = 'c1-value'
        mm['a.b.c2'] = 'c2-value'
        mm['a.b2'] = 'b2-value'
        self.assertTrue( 'a.b.c1' in mm )
        self.assertTrue( 'a.b.c2' in mm )
        self.assertTrue( 'a.b2' in mm )
        del mm['a.b.c1']
        self.assertTrue( 'a.b.c1' not in mm )
        del mm['a.b2']
        self.assertTrue( 'a.b2' not in mm )
        ## verify everything else remains
        self.assertTrue( 'a.b.c2' in mm )
        self.assertTrue( 'a.b' in mm )
        self.assertTrue( 'a' in mm )

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

    def test_simple_insertion(self):
        ll = PropList()
        ll[0] = 'zero'
        self.assertTrue( len(ll), 1 )
        self.assertTrue( 'zero' in ll )
        self.assertEqual( ll[0], 'zero' )

    def test_nested_insertion(self):
        ll = PropList()
        ll['0.a.0'] = 'zero'
        self.assertEqual( ll['0.a.0'], 'zero' )
        self.assertTrue( 'a' in ll[0] )

    def test_index_error(self):
        ll = PropList()
        self.assertEqual( len(ll), 0 )
        with self.assertRaises(IndexError):
            ll[0]
        with self.assertRaises(IndexError):
            ll['1']

    def test_simple_deletion(self):
        ll = PropList()
        ll[0] = 'zero'
        ll['1'] = 'one'
        ll[2] = 'two'
        self.assertEqual( len(ll), 3 )
        del ll[1]
        self.assertEqual( len(ll), 2 )

    def test_append(self):
        ll = PropList()
        ll.append('one')
        ll.append('two')
        ll.append('three')
        self.assertEqual( len(ll), 3 )
        self.assertEqual( ll.pop(), 'three' ) # pop from end
        self.assertEqual( len(ll), 2 )
        self.assertEqual( ll.pop(0), 'one' )  # pop from beginning
        self.assertEqual( len(ll), 1 )

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
