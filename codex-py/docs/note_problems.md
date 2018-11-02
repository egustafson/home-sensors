Codex CMDB Problems that need Resolution
========================================

A catalog of problems that need contemplation along the way.  See also
[solutions](note_solutions.md) for solutions and ideas about _some_ of these
problems.



Problem:  Decentralization of the CMDB
--------------------------------------

* don't build a monolyth -- NO monolythic patterns.  Look to etcd and
  friends for interesting patterns.
* Client proxy -- software should be able to interact locally (same
  memory space) with a degree of abstractness as to wether the CMDB is
  purely a localized instance or connected to a larger, more
  consolidated (i.e. more centralized) store.
* _Hierarchical_ partitions of authority.  In larger CMDB systems, the
  notion of planetary/galatic access to ONE CMDB should possible
  through the API, but smaller 'zones' of *localized* authority should
  exist to support both performant access and update as well as
  sometimes disconnected operation.  Look to Consul's for inspiration.


