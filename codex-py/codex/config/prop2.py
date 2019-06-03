# -*- coding: utf-8 -*-

##
##  Alternative PropMap Implementation - prop2.py
##

## Design notes & thoughts ##############################
##
## Goals:
##  * Support nested dict and array objects.
##  * Access elements & sub-trees via  "obj['key.key.index']"
##  * Access via JSON-Path
##    - https://jsonpath-rw.readthedocs.io/en/latest/
##  * Serializable to JSON
##  * De-serializable from YAML & JSON
##  * Support serialization for types:
##    - ISO8601 timestamps -> Py datetime
##    - UUID -> Py uuid.UUID
##
## Inspiration:
##  * https://configtree.readthedocs.io/en/latest/
##  * http://www.kr41.net/2015/06-15-about_configtree.html
##
##

from collections.abc import Mapping
from collections.abc import Sequence

## Note - there should be an IN-mutable base class, but the
##  code using class 'Config' does not treat the Config as
##  an inmutable object -- fix and replace class Config with
##  ConfigDO, and then make it a 'Mapping' and derive a
##  'State' class from MutableMapping.

class PropPath:
    def __init__(self, path):
        #
        # Validate path string, split and put in []
        #
        self.path = []
        self.path[0] = path

    def next():
        return self.path[0]

    def next_is_digit():
        return isinstance(self.path[0], int)

    def remainder():
        if len(self.path) > 1:
            return self.path[1:]
        else:
            return None


import re
from collections import Iterable

key_regex = "([\w\-]+)"
idx_regex = "((\.?\[\d+\])|(\d+))"
sfx_regex = "(\."+key_regex+")|("+idx_regex+")"

k_regex = "^(?P<key>"+key_regex+")(?P<sk>("+sfx_regex+")*)$"
kre = re.compile(k_regex)
i_regex = "^(?P<key>"+idx_regex+")(?P<sk>("+sfx_regex+")*)$"
ire = re.compile(i_regex)

class PropMap(Mapping):

    def __init__(self):
#        print("PropMap.__init__")
        self._data = dict()

    def load(self, *args, **kwargs):
#        print("PropMap.load()")
        self._data = dict()
        for a in args:
            if isinstance(a, Mapping):
                for (k,v) in a.items():
                    self._setitem(k,v)
            elif not isinstance(a, str) and isinstance(a, Sequence):
                for (k,v) in a:
                    self._setitem(k,v)
        for (k,v) in kwargs:
            self._setitem(k,v)
        return self

    def _splitkey(self, key):
        m = kre.fullmatch(key)
        if m is None:
            raise KeyError("Invalid key, '{}'".format(key))
        k = m.group('key')
        sk = m.group('sk').lstrip('.')
        if k is None:
            raise KeyError(key)
        return (k, sk)

    def __getitem__(self, key):
#        print("getting: {}".format(key))
        (k, sk) = self._splitkey(key)
        if sk:
            #print("get recursing:  k='{}', sk='{}'".format(k, sk))
            return self._data[k][sk]
        return self._data[k]

    def _setitem(self, key, value):
#        print("PropMap._setitem:  {} = {}".format(key, value))
        (k, sk) = self._splitkey(key)
        v = value
        if isinstance(value, Mapping):
            v = PropMap().load(value)
        if not isinstance(value, str) and isinstance(value, Sequence):
            v = PropList().load(value)
        if sk:
            if k not in self._data:
                self._data[k] = PropMap()
                #print("created sub-map")
            self._data[k]._setitem(sk,v)
        else:
            self._data[k] = v

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return dict.__repr__(dict(self))

    def _flatten(self, prefix=''):
        flat = dict()
        for (k, v) in self._data.items():
            key = k
            if len(prefix) > 0:
                key = ".".join((prefix, k))
            if isinstance(v, PropMap):
                flat.update( v._flatten(key) )
            else:
                flat[key] = v
        return flat

    def as_properties(self):
        return self._flatten()

    def as_yaml(self):
        #
        # TODO
        #
        return ""

    def as_json(self):
        #
        # TODO
        #
        return ""

    def dump(self, prefix=''):
        for (k, v) in self._data.items():
            key = k
            if len(prefix) > 0:
                key = ".".join((prefix, k))
            if isinstance(v, PropMap):
                v.dump(key)
            else:
                print("{}: {}".format(key, v))



class PropList(Sequence):
    def __init__(self):
#        print("PropList.__init__")
        self._data = list()

    def load(self, *args):
#        print("PropList.load()")
        self._data = list()
        for a in args:
            v = a
            if isinstance(a, Mapping):
                v = PropMap().load(a)
                self._data.append(v)
            elif not isinstance(a, str) and isinstance(a, Sequence):
                for ii in a:
                    self._append(ii)
        return self

    def _splitkey(self, key):
        if isinstance(key, int):
            return (key, None)
        m = ire.fullmatch(key)
        if m is None:
            raise KeyError("Invalid key, '{}'".format(key))
        k = m.group('key')
        sk = m.group('sk').lstrip('.')
        if k is None:
            raise KeyError(key)
        return (int(k.strip('[]') ), sk)

    def __getitem__(self, key):
#        print("getting: {}".format(key))
        (k, sk) = self._splitkey(key)
        if sk:
            #print("getting recursing: k='{}', sk='{}'".format(k, sk))
            return self._data[k][sk]
        return self._data[k]

    def _setitem(self, key, value):
#        print("setting: {}".format(key))
        (k, sk) = self._splitkey(key)
        v = value
        if isinstance(value, Mapping):
            v = PropMap().load(value)
        elif not isinstance(value, str) and isinstance(value, Sequence):
            v = PropList().load(value)
        if sk:
            if k not in self._data:
                self._data[k] = PropMap()
                #print("created sub-map")
            self._data[k]._setitem(sk,v)
        else:
            self._data[k] = v

    def _append(self, value):
        idx = len(self._data)
        self._data.append(None)
        self._setitem(idx, value)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return list.__repr__(list(self))

    def _flatten(self, prefix=''):
        ## TBD
        return []
