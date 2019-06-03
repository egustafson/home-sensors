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

kre = re.compile("^([\w\-]+)(\.([\w\-]+))*$")

class PropMap(MutableMapping):

    def __init__(self, *args, **kwargs):
#        print("PropMap.__init__")
        self._data = dict()
        for a in args:
            if isinstance(a, Mapping):
                for (k,v) in a.items():
                    self.__setitem__(k,v)
            elif isinstance(a, Sequence):
                for (k,v) in a:
                    self.__setitem__(k,v)
        for (k,v) in kwargs:
            self.__setitem__(k,v)

    def _splitkey(self, key):
        r = kre.match(key)
        if r is None:
            raise KeyError("Invalid key, '{}'".format(key))
        k = key.split(".", 1)
        if len (k) < 1:
            raise KeyError(key)
        if len(k) > 1:
            return (k[0], k[1])
        return (k[0], None)

    def __getitem__(self, key):
#        print("getting: {}".format(key))
        (k, sk) = self._splitkey(key)
        if sk:
#            print("get recursing:  k='{}', sk='{}'".format(k, sk))
            return self._data[k][sk]
        return self._data[k]

    def __setitem__(self, key, value):
#        print("setting:  {}".format(key))
        (k, sk) = self._splitkey(key)
        v = value
        if isinstance(value, dict):
            v = PropMap(value)
        if sk:
            if k not in self._data:
                self._data[k] = PropMap()
                #print("created sub-map")
            self._data[k][sk] = v
        else:
            self._data[k] = v

    def __delitem__(self, key):
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return dict.__repr__(dict(self))

    def _flatten(self, prefix=''):
        flat = []
        for (k, v) in self._data.items():
            key = k
            if len(prefix) > 0:
                key = ".".join((prefix, k))
            if isinstance(v, PropMap):
                flat.extend( v._flatten(key) )
            else:
                flat.append( (key, v) )
        return flat

    def flatten(self):
        return self._flatten()

    def as_properties():
        #
        # TODO
        #
        return []

    def as_yaml():
        #
        # TODO
        #
        return ""

    def as_json():
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


class PropList(MutableSequence):    ## Sequence <= list
    def __init__(self, *args):
        self._data = list(*args)
    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value
    def __delitem__(self, key):
        del self._data[key]
    def __len__(self):
        return len(self._data)
    def insert(self, i, x):
        self._data.insert(i, x)
    def flatten(self):
        ## TBD
        None


