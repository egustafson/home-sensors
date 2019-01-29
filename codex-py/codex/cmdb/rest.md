
GET   /cmdb    ??

GET   /cmdb/ci   ?? list ci oids
POST  /cmdb/ci   create new ci, initialize config[0] with json in body

GET   /cmdb/ci/[oid]  return ci object, includes list of config versions,
                        but not config's themselves.
POST  /cmdb/ci/[oid]  commit the next config[new#] with json in body.

GET   /cmdb/ci/[oid]/[ver|tag] return specified config

POST  /cmdb/ci/search  -- search and return ci's matching search
                          criteria.

--

POST  /cmdb/mo/discover  -- discover an MO based on body-json criteria

GET   /cmdb/mo    return a list of MO oids

# POST  /cmdb/mo?template=oid  -- create a MO instance based on template[oid]
#                                 return new oid for MO

GET   /cmdb/mo/[oid]  return the MO for CI[oid]
PUT   /cmdb/mo/[oid]  initialize / reset the MO's state (json body)
POST  /cmdb/mo/[oid]  update state of the MO using json body
DEL   /cmdb/mo/[oid]  remove all state (aka 'unregister') the MO

# GET   /cmdb/mo/[oid]/status  get status
# POST  /cmdb/mo/[oid]/status  set status
