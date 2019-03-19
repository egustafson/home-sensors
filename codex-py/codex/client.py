# -*- coding: utf-8 -*-
""" CMDB Client -- HTTP/S + Multicast """

from codex.config import Config

import requests

DEFAULT_URL = "http://localhost:5000"

class Client:

    def __init__(self, config):
        self.base_url = config.get('service-url', DEFAULT_URL)
        self.timeout  = config.get('timeout', 5.0)

    def healthz(self):
        """Return the Service's health check -- verify's connectivity.
             throw on timeout / comm error / non-OK or non-JSON response
        """
        url = self.base_url + "/healthz"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


    def list(self):
        """Return the complete list of CI uuid's.
             throw on timeout / comm error / non-OK or non-JSON response
        """
        url = self.base_url + "/ci"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


    def discover(self, pattern):
        """Return the 'Operating' Config of the CI matching 'identity' (a dict)."""
        url = self.base_url + "/discover"
        r = requests.post(url, json=pattern, timeout=self.timeout)
        if r.status_code == 404:
            return {}
        r.raise_for_status()
        return r.json()


    def query(self, qstr):
        """Return the results (dict or array) of the query, 'qstr'."""
        raise NotImplementedError('implementation TBD')


    def add_config(self, config, tag=None):
        """Create a new CI and initialize it with 'config'.
             return the Config w/ meta-data on success.
             throw xxxException on error.
        """
        url = self.base_url + "/ci"
        r = requests.post(url, json=config, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


    def get_config(self, id, tag=None):
        """Return Config for CI(id) or None.
             throw on timeout / comm error / non-OK or non-JSON response
        """
        url = self.base_url + "/ci/" + str(id) + "/config"
        r = requests.get(url, timeout=self.timeout)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()


    def update_config(self, id, config, tag=None):
        """Update (via appending) the CI(id)'s Config and tag if not None.
             return the Config w/ meta-data on success.
             throw on error or timeout
        """
        url = self.base_url + "/ci/" + str(id) + "/config"
        r = requests.put(url, json=config, timeout=self.timeout)
        r.raise_for_status()
        return r.json()


    def get_ci(self, id):
        """Return the ConfigInfo record."""
        url = self.base_url + "/ci/" + str(id)
        r = requests.get(url, timeout=self.timeout)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()


    def del_ci(self, id):
        """Remove the ConfigInfo(id) from the CMDB.
             throw on error.
        """
        url = self.base_url + "/ci/" + str(id)
        r = requests.delete(url, timeout=self.timeout)
        r.raise_for_status()
        return

