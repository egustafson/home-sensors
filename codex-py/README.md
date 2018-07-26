The Codex CMDB
==============

MVP for Temp Sensor
-------------------

### 1. Discover

* /discover  [POST]
* mcast "discover"

Accept a JSON record from the discoverer and return a href to the resource.

    {
      "href": "http://hostname-or-ip:port/resource/<uuid>",
      "id": "<uuid>"
      "server": "hostname-or-ip",
      "port" : port-number,
    }

### 2. Get Config

* /resource/<uuid>/config   [GET]

Return the JSON of the full config for the resource.

    {
      _"id": "<uuid>",
      "_ver": version-number,
      "_href": "http://hostname-or-ip:port/resource/<uuid>/config",

      "key1": "value1",
      "nested1" : {
        "nested-key1": numeric-value,
      }
    }

----

2nd Iteration Features
----------------------

### Get Resource

* /resource/<uuid> [GET]

Q: What all goes in this.
* the config should be the 'config' attribute.
Q: 'state' sub-dict
Q: how to handle managed state?  lookup ITU spec vCMDB uses.
   - maybe a _single_ attr with complex state transitions?
