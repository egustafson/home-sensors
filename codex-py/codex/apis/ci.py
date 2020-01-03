# -*- coding: utf-8 -*-
"""REST API (route) for Configuration Information (ci)"""

from flask_restplus import Namespace, Resource

ns = Namespace('ci', description='Configuration Information endpoint')

@ns.route('/search')
@ns.response(404, 'Config not found')
class ConfigSearch(Resource):
    @ns.doc('search for Config(s)')
    def post(self):
        '''search for config(s)'''
        #
        # TODO
        #
        return []


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
        return { 'type': 'ci record' }

    @ns.doc('commit new version of Config')
    def post(self, id):
        #
        # Stub
        #
        return { 'type': 'ci record' }


@ns.route('/<uuid:id>/<ver>')
@ns.param('id', 'UUID of the Config')
@ns.param('ver', 'version number or tag-id')
@ns.response(404, 'Config not found')
class Config(Resource):
    @ns.doc('return config')
    def get(self, id, ver):
        #
        # TODO
        #
        return {}

