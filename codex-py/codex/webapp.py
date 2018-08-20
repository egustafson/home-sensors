# -*- coding: utf-8 -*-
""" Web-App defnition and factory
     Uses: Flask & Flask-RESTFul
"""

from flask import Flask, request, jsonify
from flask_restful import abort, Api
from flask_restful import Resource as RESTResource

from codex import view, healthz
from codex.settings import ProdConfig
from codex.cmdb import CMDB

_cmdb = CMDB()


class ResourceList(RESTResource):
    def get(self):
        abort(500, message="TBD - no implementation")

class Discover(RESTResource):

    def post(self):
        identity = request.get_json()
        meta = _cmdb.discover(identity)
        if meta is None:
            abort(404, message="no resource with that identity discovered")
        return jsonify(meta)

class Resource(RESTResource):
    def get(self, rid):
        abort(500, message="--*-- MISSING IMPL --*-- requested resource, (id={}), does not exist.".format(rid))


class Config(RESTResource):
    def get(self, rid):
        cfg = _cmdb.get_config(rid)
        if cfg is None:
            abort(404, message="requested resource, (id={}), does not exist.".format(rid))
        return jsonify(cfg)

    def put(self, rid):
        cfg = request.get_json()
        print(cfg)
        meta = _cmdb.set_config(rid, cfg)
        if meta is None:
            abort(500, message="error setting config.")
        return jsonify(meta)

class LinkList(RESTResource):
    def get(self):
        abort(500, message="TBD - no implementation")

class Link(RESTResource):
    def get(self, lid):
        abort(500, message="TBD - no implementation")



def create_app(config_object=ProdConfig):
    """Flask applicaton factory
    """
    webapp = Flask(__name__.split('.')[0])
    restapi = Api(webapp)

    webapp.url_map.strict_slashes = False
    webapp.config.from_object(config_object)

    restapi.add_resource(ResourceList, '/resource')
    restapi.add_resource(Resource, '/resource/<uuid:rid>')
    restapi.add_resource(Config, '/resource/<uuid:rid>/config')
    restapi.add_resource(Discover, '/discover')
    ##
    ## ...
    ##

#    webapp.register_blueprint(view.blueprint)
#    webapp.register_blueprint(healthz.blueprint)
    return webapp

