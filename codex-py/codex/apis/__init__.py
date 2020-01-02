# -*- coding: utf-8 -*-

from flask_restplus import Api

from .healthz import ns as ns_hz
from .ci import ns as ns_ci
from .mo import ns as ns_mo

api = Api(
    title='CODEX CMDB',
    version='1.0',
    description='The CODEX CMDB'
)

api.add_namespace(ns_hz)
api.add_namespace(ns_ci)
api.add_namespace(ns_mo)


