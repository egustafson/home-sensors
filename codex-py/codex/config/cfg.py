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
from collections.abc import Sequence

## Note - there should be an IN-mutable base class, but the
##  code using class 'Config' does not treat the Config as
##  an inmutable object -- fix and replace class Config with
##  ConfigDO, and then make it a 'Mapping' and derive a
##  'State' class from MutableMapping.

class ConfigMap(MutableMapping):
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

class ConfigList(Sequence):    ## Sequence <= list
    pass


class Config(ConfigMap):
    def __init__(self, *args, **kwargs):
        self._validated = False
        self._dirty = False
        super().__init__(*args, **kwargs)
    @property
    def dirty(self):
        return self._dirty
    @property
    def validated(self):
        return self._validated



class Cref(ConfigMap): pass
    # holds a reference to a config / CI
    #
    # { # Cref
    #   id:  <config/CI-uuid>
    #   tag: <ci-tag>  ## optional
    #   rel: "text-relationship-descriptor" # optional
    #   obj: { object referenced -- caching / python 'ref' }
    #   ...???...
    # }

