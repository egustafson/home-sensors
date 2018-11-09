# -*- coding: utf-8 -*-
""" Managed Object """

class ManagedObject: pass
    # Extends AND abstracts a ConfigItem
    #  * Represents an object under management. Not
    #     all CI's are MO's, all MO's are 1:1 w/ a CI
    #  * (idea) returns a flattened hierarchy of CI's,
    #     which makes it easier on a running MO to load
    #     it's configuration.
    #  * MO holds the MO's _state_, in addition to
    #     referencing the MO's _configuration_.
    #
    #  {  # MO
    #    config-item:  <uuid-of-CI>
    #    state: { obj of state }
    #    ...???...
    #  }

