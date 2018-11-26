# -*- coding: utf-8 -*-
""" Managed Object """

class ManagedObject:
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

    def __init__(self, id):
        self._id = id
        self._config = None
        self._state = None

    @property
    def id(self):
        return self._id

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
