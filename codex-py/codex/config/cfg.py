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

from codex.config.prop import PropMap
from codex.config.prop import PropList

class Config(PropMap):
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



class Cref(PropMap): pass
    # holds a reference to a config / CI
    #
    # { # Cref
    #   id:  <config/CI-uuid>
    #   tag: <ci-tag>  ## optional
    #   rel: "text-relationship-descriptor" # optional
    #   obj: { object referenced -- caching / python 'ref' }
    #   ...???...
    # }

