Possible Soutions to Codex CMDB Architecture
============================================

A catalog of solutions to problems and solutions looking for a problem
in the context of the Codex CMDB.

Configuration Item and Managed Object
-------------------------------------

The ITOM and MIB world has _similar_, but not identical notions of
things to be managed.  Both patterns leave gaps the other fills.  The
following attempts to merge the two worlds and create a more
comprehensive solution while still afording each model's simplicity
where appropriate.

* Configuration Item (CI) -- A managed configuration thing.
* Configuration (Config) -- A descrite configuration.  An instance of a
  configuration specifically.
* Managed Object (MO) -- A thing that is often handled in a way consistent
  with managing it.  Very often an Active Object, but not always.  A
  managed object should always have state _and_ configuration.
* State - The reality of a thing.  "How it is" vs "How it should be"
  (i.e. configuration).

