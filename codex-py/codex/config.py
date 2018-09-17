# -*- coding: utf-8 -*-
""" CMDB Config object """

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


class Config(dict): pass
""" A configuration object
      - initially a dict (a hack).
      - see comments above.
"""
