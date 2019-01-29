# -*- coding: utf-8 -*-

from codex.config.prop import PropMap2 as PropMap
from codex.config.prop import PropList as PropList


tmap = { "k1": "v1",
         "k2": "v2",
         "k3": {"k3a": "v3a"},
         "k4": {"k4a": {"k4b": "v3b"}},
#         "k5": {"K$5": "v5a"},
#         "k6.k6a": "v6a",
       }

pmap = PropMap(tmap)

#print("tmap: {}".format(tmap))
#print("pmap: {}".format(pmap))

pmap.dump()
print("")

print("pmap is a {}".format(pmap.__class__))
print("pmap[k3] is a {}".format(pmap["k3"].__class__))

pmap["k9.k9a.k9b"] = "v9"

print("index k1: {}".format(pmap["k1"]))
# print("index kk: {}".format(pmap["kk"]))
print("index k3.k3a: {}".format(pmap["k3.k3a"]))
print("index k4.k4a.k4b: {}".format(pmap["k4.k4a.k4b"]))

try:
    print("index k1: {}".format(pmap["k1"]))
except KeyError as ex:
    print("ex: {}".format(ex))

print("")
pmap.dump()
