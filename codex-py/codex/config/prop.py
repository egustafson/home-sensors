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

class PropMap(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._data = dict(*args, **kwargs)
    def __getitem__(self, key):
        return self._data[key]
    def __setitem__(self, key, value):
        self._data[key] = value
    def __delitem__(self, key):
        del self._data[key]
    def __iter__(self):
        return iter(self._data)
    def __len__(self):
        return len(self._data)

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


