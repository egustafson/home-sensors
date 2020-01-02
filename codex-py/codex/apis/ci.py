# -*- coding: utf-8 -*-
"""REST API (route) for Configuration Information (ci)"""

from flask_restplus import Namespace, Resource

ns = Namespace('ci', description='Configuration Information endpoint')

@ns.route('/')
class ConfigItemList(Resource):
    @ns.doc('list ci uuids')
    def get(self):
        '''return a list of ci uuids'''
        #
        # Stub
        #
        return []

    @ns.doc('create a new ci')
    def post(self):
        '''create a new ci, return UUID'''
        #
        # Stub
        #
        return 'UUID-PLACEHOLDER'

@ns.route('/<uuid:id>')
@ns.param('id', 'UUID of the ConfigItem')
@ns.response(404, 'CI not found')
class ConfigItem(Resource):
    @ns.doc('return ci metadata')
    def get(self, id):
        #
        # Stub
        #
        return { }

    @ns.doc('commit new version of Config')
    def post(self, id):
        #
        # Stub
        #
        return
