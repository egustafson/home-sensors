# -*- coding: utf-8 -*-

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

from collections.abc import Mapping, MutableMapping
from collections.abc import Sequence, MutableSequence

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

key_regex = r'([\w\-]+)'
idx_regex = r'((\[\d+\])|(\d+))'
sfx_regex = r'(\.'+key_regex+r')|(\.?'+idx_regex+r')'

k_regex = r'^(?P<key>'+key_regex+r')(?P<sk>('+sfx_regex+r')*)$'
kre = re.compile(k_regex)
i_regex = r'^(?P<key>'+idx_regex+r')(?P<sk>('+sfx_regex+r')*)$'
ire = re.compile(i_regex)

def splitkey(key):
    if isinstance(key, int):
        return (key, None)
    # else
    m = ire.fullmatch(key)
    if m is not None:
        k = m.group('key')
        sk = m.group('sk').lstrip('.')
        if k is None:
            raise KeyError(key)
        return (int(k.strip('[]')), sk)
    # else
    m = kre.fullmatch(key)
    if m is not None:
        k = m.group('key')
        sk = m.group('sk').lstrip('.')
        if k is None:
            raise KeyError(key)
        return (k, sk)
    # else
    raise KeyError("Invalid key, '{}'".format(key))

def mksubkeytype(subkey):
    (k, sk) = splitkey(subkey)
    if isinstance(k, int):
        return PropList()
    else:
        return PropMap()

class PropMap(MutableMapping):

    def __init__(self):
#        print("PropMap.__init__")
        self._data = dict()

    def load(self, *args, **kwargs):
#        print("PropMap.load()")
        self._data = dict()
        for a in args:
            if isinstance(a, Mapping):
                for (k,v) in a.items():
                    self.__setitem__(k,v)
            elif not isinstance(a, str) and isinstance(a, Sequence):
                for (k,v) in a:
                    self.__setitem__(k,v)
        for (k,v) in kwargs:
            self.__setitem__(k,v)
        return self

    def __getitem__(self, key):
#        print("getting: {}".format(key))
        (k, sk) = splitkey(key)
        if sk:
            #print("get recursing:  k='{}', sk='{}'".format(k, sk))
            return self._data[k][sk]
        return self._data[k]

    def __setitem__(self, key, value):
#        print("PropMap._setitem:  {} = {}".format(key, value))
        (k, sk) = splitkey(key)
        v = value
        if isinstance(value, Mapping):
            v = PropMap().load(value)
        if not isinstance(value, str) and isinstance(value, Sequence):
            v = PropList().load(value)
        if sk:
            if k not in self._data:
                self._data[k] = mksubkeytype(sk)
                #print("created sub-element")
            self._data[k].__setitem__(sk,v)
        else:
            self._data[k] = v

    def __delitem__(self, key):
        (k, sk) = splitkey(key)
        if sk:
            del self._data[k][sk]
        else:
            del self._data[k]

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
            elif isinstance(v, PropList):
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



class PropList(MutableSequence):
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

    def __getitem__(self, key):
#        print("getting: {}".format(key))
        (k, sk) = splitkey(key)
        if sk:
            #print("getting recursing: k='{}', sk='{}'".format(k, sk))
            return self._data[k][sk]
        return self._data[k]

    def __setitem__(self, key, value):
#        print("setting: {}".format(key))
        (k, sk) = splitkey(key)
        if not isinstance(k, int):
            raise KeyError("Key is not an int")
        while len(self._data) < k+1:
            self._data.append(None)
        v = value
        if isinstance(value, Mapping):
            v = PropMap().load(value)
        elif not isinstance(value, str) and isinstance(value, Sequence):
            v = PropList().load(value)
        if sk:
            if k not in self._data:
                self._data[k] = mksubkeytype(sk)
                #print("created sub-element")
            self._data[k].__setitem__(sk,v)
        else:
            self._data[k] = v

    def insert(self, key, value):
        (k, sk) = splitkey(key)
        if not isinstance(k, int):
            raise KeyError("Key is not an int")
        if sk:
            if k >= len(self._data):
                k = len(self._data)
            self._data.insert(k, None)
            self.__setitem__("{}.{}".format(k,sk),v)
        else:
            self._data.insert(k, value)

    def __delitem__(self, key):
        (k, sk) = splitkey(key)
        if sk:
            del self._data[k][sk]
        else:
            del self._data[k]

    def _append(self, value):
        idx = len(self._data)
        self._data.append(None)
        self.__setitem__(idx, value)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return list.__repr__(list(self))

    def _flatten(self, prefix=''):
        flat = dict()
        ii = 0
        for v in self._data:
            key = "{}[{}]".format(prefix, ii)
            ii += 1
            if isinstance(v, PropMap):
                flat.update( v._flatten(key) )
            elif isinstance(v, PropList):
                flat.update( v._flatten(key) )
            else:
                flat[key] = v
        return flat
