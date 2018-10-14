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

### 2. List Configuration Items (CI's)

* /ci  [GET]

Return a list of CI uuid's

    [
      16e448fa-cffc-11e8-9353-000c29b7f6e5
      c6e448fa-cffc-11e8-9353-000c29b7f6e5
      26e448fa-cffc-11e8-9353-000c29b7f6e5
      36e448fa-cffc-11e8-9353-000c29b7f6e5
    ]

### 3. Get Config

* /ci/\<uuid\>/config   [GET]

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

### 4. Put Config

* /ci/\<uuid\>/config [PUT]

### 5. Delete Configuration Item (CI)

* /ci/\<uuid\> [DEL]

### 6. healthz - monitoring resource

* /healthz [GET]

----

2nd Iteration Features
----------------------

### Get Configuration Item (CI)

* /resource/\<uuid\> [GET]

Q: What all goes in this.
* the config should be the 'config' attribute.
Q: 'state' sub-dict
Q: how to handle managed state?  lookup ITU spec vCMDB uses.
   - maybe a _single_ attr with complex state transitions?
