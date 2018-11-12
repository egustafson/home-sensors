# -*- coding: utf-8 -*-
""" CMDB Config object """

import yaml

from codex.config.ci import ConfigItem
from codex.config.mo import ManagedObject

from codex.config.cfg import Config


class CTempl: pass
    # Config typing / validation system -- mix-ins.

def load(s):
    d = yaml.load(s)
    return Config(d)
