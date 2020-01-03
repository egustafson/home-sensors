# -*- coding: utf-8 -*-
#
#   Copyright (c) 2018 Eric Gustafson
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
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
