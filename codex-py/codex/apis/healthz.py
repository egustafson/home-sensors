# -*- coding: utf-8 -*-
"""REST API (route) for /healthz"""

from flask_restplus import Namespace, Resource

ns = Namespace('healthz', description='health reporting endpoint')

@ns.route('/')
class HealthZ(Resource):
    @ns.doc('report health')
    def get(self):
        '''return application health'''
        #
        # Stub
        #
        return { 'status': "ok" }
