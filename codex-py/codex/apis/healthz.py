# -*- coding: utf-8 -*-
"""REST API (route) for /healthz"""

from codex.healthz import Healthz
from flask_restplus import Namespace, Resource

ns = Namespace('healthz', description='health reporting endpoint')

HZ = Healthz()

@ns.route('/')
class HealthZ(Resource):
    @ns.doc('report health')
    def get(self):
        '''return application health'''
        return HZ.status()
