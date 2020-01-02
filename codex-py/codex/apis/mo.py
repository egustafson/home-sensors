#-*- coding: utf-8 -*-
""" REST API (route) for /mo """

from flask_restplus import Namespace, Resource

ns = Namespace('mo', description='managed object (mo) endpoint')

@ns.route('/')
class ManagedObjList(Resource):
    @ns.doc('list mo uuids')
    def get(self):
        '''return a list of mo uuids'''
        #
        # Stub
        #
        return []

@ns.route('/discover')
class DiscoverMO(Resource):
    @ns.doc('search for a MO')
    def post(self):
        '''search for a MO'''
        #
        # TODO
        #
        return { }

@ns.route('/<uuid:id>')
@ns.param('id', 'UUID of the Managed Object')
@ns.response(404, 'MO not found')
class ManagedObj(Resource):
    @ns.doc('return MO')
    def get(self, id):
        '''return existing MO'''
        #
        # TODO
        #
        return {}

    @ns.doc('initialize MO (from CI)')
    def put(self, id):
        '''initialize a CI -> MO'''
        #
        # TODO
        #
        return { }

    @ns.doc('update MO state')
    def post(self, id):
        '''update MO'''
        #
        # TODO
        #
        return { }

    @ns.doc('deregister MO')
    def delete(self, id):
        '''deregister (delete) MO'''
        #
        # TODO
        #
        return '', 204
